# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 10:47:36 2020

@author: Guenole CHEROT
"""
import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import Bounds
import osqp
from scipy import sparse
from copy import deepcopy


#############################
#### A JOUTER A CE CODE #####
#############################
"""
Attribu :
    - Fréquence de mise à jour du prix

fonction :
    - agent.warm_copy(max_it) # créer une copie de l'agent mais dont la série temporel est constante

"""

#############################

class Agent():
    
    ########################################################################################################
    ############################################# INIT and  SETERS #########################################
    ########################################################################################################
    
    """Agent which are part of the network. \n
    Input :
        - name (str) : Name of the agent
        - ID (int) : Unique id of the agent
        - element (int) : ID used in panda_power
        - et (str) : Type of the agent ('load', 'gen', 'ext_grid')
        - bus (int) : connected to bus n
        - n_agent (int) : Total number of agent on the grid
        - grid_cost_type (str,'uniq') : type of grid cost imposed by the SO. Can be : 'uniq', 'zone'
        - zone (int) : zone of the agent
        - flexibility (float) : How much this agent is flexible (for now the flexibility is fixed throughout the simulation)
        - rho (float) : Penalty factor of the ADMM (can be set manually for better convergence or privacy.)
        - time_series (DataFrame) : Power consumed by the agent during the simulation.
        - partner (array) : list of other agent ID this agent is allowed to trade with.
        """
    def __init__(self, name, ID, element, et, bus, n_agent, grid_cost_type, zone, flexibility, rho, time_series,
                 partners="all"):
        self.name = name
        self.ID = ID
        self.element = element
        self.et = et
        self.bus = bus
        self.n_agent = n_agent
        self.grid_cost_type = grid_cost_type
        self.zone = zone
        self.flex = flexibility
        self.rho = rho
        self.time_series = time_series
        self.partners = partners
        if self.partners == "all":
            self.partners = np.linspace(0,self.n_agent-1, self.n_agent, dtype=int)

        # time
        self.t = 0
        # power proposed by the agent
        self.P1 = np.zeros(self.n_agent)
        # counter proprosition of power by the other agents
        self.P2 = np.zeros(self.n_agent)
        # Dual variable of the problem
        self.dual = np.zeros(self.n_agent)
        # Set all bounds and poly_cost
        self.update_current_values()
        # Init grid cost at 0
        self.grid_cost = 0
        
    
    ########################################################################################################
    ########################################### Update Functions ###########################################
    ########################################################################################################
    
    def update_current_values(self):
        # Update the objective power
        self.p = 1e-3*self.time_series[self.time_series["time"]==self.t]["grid"].values[0] # multiply by 1e-3 because the power is in kW
        # Update the bound for this agent
        self.update_bounds()
        # Update the bound taking parteners into account
        self.update_bounds_partners()
        # Update the polycost based on the flexibility and objective power
        self.update_poly_cost()
    
    def update_bounds(self):
        p = self.p
        
        self.min_q_mvar = 0
        self.max_q_mvar = 0
       
        if self.et == "load":
            if p < 0 :
                self.min_p_mw = 2*p # p*(1+1/flex)
                self.max_p_mw = 0 # min(0, p*(1-1/flex))
            if p >= 0 :
                self.min_p_mw = 0 # p*(1-1/flex) # max(0, p*(1-1/flex))
                self.max_p_mw = 2*p # p*(1+1/flex)
        elif self.et == "ext_grid":
            self.min_p_mw = -5
            self.max_p_mw = 5
        else :
            raise ValueError("{0} is not in ['ext_grid','gen','load']")
    
    def update_bounds_partners(self):
        """Set linar bounds on p_nm for the agent n"""
        Min = np.zeros(self.n_agent) # Minimum power that can be exchange with other agents
        Max = np.zeros(self.n_agent) # Maximum power that can be exchange with other agents
        # Bounds on p_nm, self.partners represents all partners the agent can exange with (if no partners, Min = [0, ...,0] and  Max = [0, ...,0], no exchanges possible)
        Min[self.partners] = -np.inf
        Max[self.partners] = np.inf
        self.bounds = Bounds(Min,Max)
        
    def update_poly_cost(self):
        """Compute the polycost associated with the desired power of the agent.
        Definition :
            - polycost (array) : array constaining coeff of the cost function (f = a + b*x + c*x**2)"""
        p = self.p
        flex = self.flex
        self.polycost = [0,-2*p*flex,flex]
        
    ########################################################################################################
    ############################################# Build gamma ##############################################
    ########################################################################################################

    def build_gamma(self):
        """Build the matrix gamma representing the distance between each agent.
        Gamma is size (n_agent,n_agent).
        Input :
            - grid_cost_type (str,'uniq') : type of grid cost imposed by the SO. Can be : 'uniq', 'zone'
            - mode (str, 'Thevenin') : Method to compute the electrical distance in the network. Two electrical distances are possible : 'Thevenin' or 'PTDF'
        """
        # sign before gamma (so that the product gamma*p_nm is always positive)
        if self.p < 0:
            sign = -1
        else :
            sign = 1
        
        if self.grid_cost_type == 'uniq' :
            gamma = sign*np.ones(self.n_agent)
        if self.grid_cost_type == 'zone':
            gamma = np.zeros(self.n_agent)
            for m in range(self.n_agent):
                gamma[m] = sign*self.zone(self.ID, m)
        
        # Take the grid price into account
        self.gamma = self.grid_cost*gamma
    
    def zone(self,n,m):
        """return if the agent n and m are in the same zone. \n
        Input :
            - n (int) : agent n
            - m (int) : agent m
            
        Output :
            - 1 if the agents are in the same zone
            - 0 if not
            """
        raise ValueError("To be implemented")
        
    ########################################################################################################
    ################################### Communication with panda network ###################################
    ########################################################################################################
    
    def send_polycost_to_grid(self):
        """Set a new value to the polycost. (change the preference of the agent)
        The polycost are in the format of pandapower (we inverse in case of load for the ADMM)
        Output :
            - polycost (array) : array [a, b, c] constaining coeficient of the cost function (f = a + b*x + 0.5*c*x**2), with the good sign for panda_power"""
        polycost = deepcopy(self.polycost)
        if polycost[1] < 0 : # Power consumed by the agent
            polycost[1] += self.grid_cost
            grid_cost = self.grid_cost
        else :
            polycost[1] -= self.grid_cost
            grid_cost = -self.grid_cost
        
        if self.et == "load":
            polycost[1] *= -1
            polycost[2] *= -1
        return polycost, grid_cost
    
    def send_bounds_to_grid(self):
        """Set a new value to the polycost. (change the preference of the agent)
        The polycost are in the format of pandapower (we inverse in case of load for the ADMM)
        Output :
            - polycost (array) : array [a, b, c] constaining coeficient of the cost function (f = a + b*x + 0.5*c*x**2), with the good sign for panda_power"""
        if self.et == "load":
            min_p_mw, max_p_mw = -self.max_p_mw, -self.min_p_mw
        else :
            min_p_mw, max_p_mw = self.min_p_mw, self.max_p_mw
        return min_p_mw, max_p_mw

    ########################################################################################################
    ############################################ Core functions ############################################
    ########################################################################################################
    
    def run(self, warm_start = False):
        """Performs one step of the ADMM process.
        Input :
            - warm_start (bool) : : Performs a warm start if True (stop the time for this agent so it performs with always the same objective power)
        Output :
            - power (float) : total power consumed be the agent
            - min_p_mw, max_p_mw, polycost : new preference of the agent (only for OPF)"""
        self.update_dual()
        self.update_current_values()
        self.minimization()
        
        # time
        if warm_start == False :
            self.t += 1
        
        # Send to network
        polycost, grid_cost = self.send_polycost_to_grid()
        min_p_mw, max_p_mw = self.send_bounds_to_grid()
        
        return self.P1, min_p_mw, max_p_mw, polycost, grid_cost
    
    def update_trade_and_price(self, trade, grid_cost):
        """Update the trades proposed by other agents and network fees. \n
        Input :
            - trade (array) : array of shape (n_agent) representing the trade wanted by all other agents.
            - grid_cost (float) : cost imposed by the DSO."""
        self.P2 = trade
        self.grid_cost = grid_cost
        if self.et == "ext_grid" :
            self.grid_cost = 0
        self.build_gamma()
    
    def update_dual(self):
        """Update the Dual variable of the optimisation by looking at trades proposed by other agents. \n
        """
        self.dual -= (self.rho/2)*(self.P1+self.P2)
        
    def minimization(self):
        """Return the matrix that minimises the cost for the agent n. \n
        Output :
            - P (array) : Matrix size (n_agent,n_agent) representing the power trade between the agent n and the other agents"""  
        N = self.n_agent
        # Function to minimize
        b, c = self.polycost[1:3]
        Z = 0.5*(self.P1-self.P2)
        # Matrix for OSQP
        P = self.rho*sparse.eye(N) + 2*c*sparse.csr_matrix(np.ones((N,N)))
        q = self.gamma - self.dual - self.rho*Z + b*np.ones(N)
        A = sparse.vstack([sparse.csc_matrix(np.ones(N)),sparse.eye(N)], format='csc')
        l = np.hstack([self.min_p_mw,self.bounds.lb])
        u = np.hstack([self.max_p_mw,self.bounds.ub])
        m = osqp.OSQP()
        m.setup(P=P, q=q, A=A, l=l, u=u, verbose=False)
        results = m.solve()
        self.P1 = results.x
        return results.x

    def n_simu(self):
        """Return the number of time step of the simulation."""
        return(self.time_series.time.size)
    
    ########################################################################################################
    ################################################## PLOTS ###############################################
    ########################################################################################################    

    def __repr__(self):
        """Give usefull information about agent n."""
        # General info
        ret = "Agent n° " + str(self.ID) +"\n"
        ret += "zone : " + str(self.zone)+"\n"
        ret += "type : " + str(self.et)+"\n"
        ret += "Maximum power : " + str(self.max_p_mw)+" MW \n"
        ret += "Minimum power : " + str(self.min_p_mw)+" MW \n"
        ret += "Minimum of the cost function : " + str(-self.polycost[1]/(2*self.polycost[2])) + " MW \n"
        ret += "Flexibility : " + str(self.flex) + "\n"
        ret += "Rho : " + str(self.rho)
        return ret
        
    def plot_cost(self):
        """Plot the cost function of the agent."""
        a, b, c = self.polycost[0:3]
        if self.et == "ext_grid":
             P = np.linspace(0,1000, 100)
        else :
            min_p = -b/(2*c)
            P = np.linspace(min(2*min_p,0),max(2*min_p,0), 100)
        plt.plot(P,a + b*P + c*np.square(P))
        plt.grid()
        plt.title("Cost function of the agent {0}".format(self.ID))
        plt.xlabel("Power (MW)")
        plt.ylabel("Cost (€)")
        plt.show()
        
    def plot_gamma(self):
        """Plot the aditionnal cost impossed by the SO to the agent."""
        self.build_gamma()
        M = np.linspace(0,self.n_agent-1,self.n_agent)
        plt.bar(M, self.gamma)
        plt.title("Peer to peer cost imposed by SO to agent {0}".format(self.ID))
        plt.xlabel("agent m")
        plt.ylabel("Gamma (€/MW)")
        plt.grid()
        plt.show()
        
    def plot_bounds(self):
        """Plot the bounds of the power trades"""
        M = np.linspace(0,self.n_agent-1,self.n_agent)
        plt.bar(M, height=self.bounds.ub-self.bounds.lb, bottom=self.bounds.lb)
        plt.title("possible trade between agent {0} and agent m".format(self.ID))
        plt.xlabel("agent m")
        plt.ylabel("power trade possible (MW)")
        plt.grid()
        plt.show()
    
    def plot_power_trade(self):
        """Plot the power exanged to all the other agents."""
        # Plot the cost function 
        M = np.linspace(0,self.n_agent-1,self.n_agent)
        plt.bar(M, self.P1)
        plt.grid()
        plt.title("Power exchanged from agent {0} to agent m".format(self.ID))
        plt.xlabel("Power (MW)")
        plt.ylabel("agent m")
        plt.grid()
        plt.show()
        