# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 11:10:02 2021

@author: Guenole CHEROT
"""

import numpy as np
import warnings
from tqdm import tqdm
from joblib import Parallel, delayed
warnings.filterwarnings("ignore")

import pandapower as pp

from rt_congestion_control.memory import Memory
from rt_congestion_control.agent import Agent

class Admm():
    """Take all actors and perform the ADMM. \n
    Input :
        - Net : instance of the Network class panda_power
        - SO : instance of System opérator class
        - Communication : instance of the Communication class
        - rho (float) : Penalisation parameter of the ADMM
        - compute_opf (int, 1) : 0 does not compute OPF, 1 compute OPF with line limits, 2 compute OPF with and without line limits
        """
        
    ########################################################################################################
    ########################################### INIT and  SETERS ###########################################
    ########################################################################################################
    
    def __init__(self, net, SO, communication, rho=1000, compute_opf=1):
        self.net = net
        self.init_net()
        self.SO = SO
        self.communication = communication
        self.rho = rho
        self.compute_opf = compute_opf
        
        # Other usefull variables
        self.n_load = len(self.net.load)
        self.n_agent = self.n_load +1 #Add the ext grid
        self.n_step = len(self.net.data[self.net.data["dataid"]==1])
        
        # Create the agents
        self.create_agents(net.data)
        self.memory = self.init_memory(self.agents, SO)
        
    def create_agents(self, time_series):
        """Create all the agents (prosumer).
        Input :
            - time_series (DataFrame) : Contains the power asked by each agent trough time."""
        self.agents = []
        for k in self.net.flex_data.index:
            ID = self.net.flex_data.dataid[k]
            self.agents.append(Agent(name=None,
                                     ID=ID,
                                     element=ID,
                                     et=self.net.flex_data.et[k],
                                     bus=self.net.flex_data.bus[k],
                                     n_agent=self.n_agent,
                                     zone=self.net.flex_data.zone[k],
                                     flexibility=self.net.flex_data.flexibility[k],
                                     grid_cost_type = "uniq",
                                     rho=self.rho,
                                     partners="all",
                                     time_series=self.net.data[self.net.data["dataid"]==ID].sort_values(by='time')))
            
    def init_memory(self, agents, SO, n_step_warm=None):
        """Initialise a memory to store all data from the simulation.
        Can be used to store data from warm start.
        Input :
            - agets (list) : list of Agent
            - SO : instance of System opérator class
            - n_step_warm (int, None) : Number of iteration of the warm start, if the memory is used for warm start."""
        if n_step_warm == None :
            n_step = self.n_step
        else :
            n_step = n_step_warm
            
        memory = Memory(n_agent = self.n_load +1, #ext_grid is couted as a agent
                             n_step = n_step,
                             n_line = len(self.net.line),
                             n_bus = len(self.net.bus),
                             grid_cost_type=self.SO.grid_cost_type,
                             line_limits = self.SO.line_limits,
                             compute_opf=self.compute_opf,
                             data=self.net.data,
                             flex_data = self.net.flex_data)
        return memory
    
    def init_load(self):
        """Create a load at each bus where a prosumer is."""
        # Delete old load
        for k in self.net.load.index :
            self.net.load.drop(k, inplace=True)
        # Create new loads
        for k in self.net.flex_data.loc[self.net.flex_data["et"]=="load"].dataid:
            pp.create_load(net = self.net,
                           bus = self.net.flex_data.loc[self.net.flex_data["dataid"]==k].bus.values[0],
                           index = k,
                           p_mw = self.net.data[self.net.data["dataid"]==k].sort_values(by='time')['grid'].iloc[0],
                           controllable = True)
            
    def init_bounds(self):
        """Initialize the bound in pandapower network"""
        # for load
        for k in self.net.flex_data.loc[self.net.flex_data["et"]=="load"].dataid :
            p = -1e-3*self.net.data[self.net.data["dataid"]==k].sort_values(by='time')['grid'].iloc[0]
            if p >= 0 :
                self.net.load.at[k,"min_p_mw"] = 0
                self.net.load.at[k,"max_p_mw"] = 2*p
            if p < 0 :
                self.net.load.at[k,"min_p_mw"] = 2*p
                self.net.load.at[k,"max_p_mw"] = 0
            self.net.load.at[k,"min_q_mvar"] = 0
            self.net.load.at[k,"max_q_mvar"] = 0
            
            # required to run power flow
            self.net.load.at[k,"p_mw"] = p
        
        # For ext_grid
        self.net.ext_grid["min_p_mw"] = -50
        self.net.ext_grid["max_p_mw"] = +50
        self.net.ext_grid["min_q_mvar"] = -1
        self.net.ext_grid["max_q_mvar"] = 1
        
    def init_poly_cost(self, ext_grid_cost=0.1):
        """Initialize the polycost in panda power network"""
        # Delete old poly_cost
        for k in self.net.poly_cost.index :
            self.net.poly_cost.drop(k, inplace=True)
            
        pp.create_poly_cost(self.net, 0, 'ext_grid',cp0_eur=1, cp1_eur_per_mw=0, cp2_eur_per_mw2=ext_grid_cost)
        
        for k in self.net.flex_data.loc[self.net.flex_data["et"]=="load"].dataid:
            p = -1e-3*self.net.data[self.net.data["dataid"]==k].sort_values(by='time')['grid'].iloc[0]
            flex = self.net.flex_data["flexibility"][self.net.flex_data.dataid==k].iloc[0]
            pp.create_poly_cost(self.net, k, 'load',
                                cp1_eur_per_mw= -2*p*flex,
                                cp2_eur_per_mw2= -flex)
            
    def init_net(self):
        self.init_load()
        self.init_bounds()
        self.init_poly_cost()
    
    ########################################################################################################
    ######################################## Network manipulations #########################################
    ########################################################################################################
        
    def update_network(self, trade, min_p_mw, max_p_mw, polycost):
        """Update the network with power aplied by agents.
        Input :
            - trade (array) : array of size (n_agent, n_agent) contaning all the trade computed by the agents
            - min_p_mw (array) : array of size (n_agent) representing the lower bound for each agent
            - max_p_mw (array) : array of size (n_agent) representing the upper bound for each agent
            - polycost (array) : array of size (n_agent, 3) representing the polynomial cost for each agent"""
        self.update_net_power(np.sum(trade, axis=1))
        self.update_bounds(min_p_mw, max_p_mw)
        self.update_polycost(polycost)
        
    def update_net_power(self, power):
        """Update the power produced by each agent in the panda_power network. Should be done after ADMM and before load flow. \n
        Input :
            - power (array) : vector size (n_agent) representing the power consumed by each agent."""
        # Make shure the total power balance is null (the exess is provided by the network)
        power[0] = -np.sum(power[1:]) # This line assumes that the first agent is the external grid
        
        # Change the sign because the power is alway positive in panda power
        for k in self.net.flex_data.loc[self.net.flex_data["et"]=="load"].dataid:
            self.net.load["p_mw"][k] = -power[k] # For loads : positive power means consumed
            

    def update_bounds(self, min_p_mw, max_p_mw):
        """Update the bounds of each agents. \n
        Input :
            - min_p_mw (array) : array of size (n_agent) representing the lower bound of each agent
            - max_p_mw (array) : array of size (n_agent) representing the upper bound of each agent"""
        for k in self.net.flex_data.index:
            ID = self.net.flex_data.dataid[k]
            if self.net.flex_data.et[k] == "load":
                self.net.load["min_p_mw"][ID] = min_p_mw[ID]
                self.net.load["max_p_mw"][ID] = max_p_mw[ID]
            elif self.net.flex_data.et[k] == "ext_grid":
                self.net.ext_grid["min_p_mw"][ID] = min_p_mw[ID]
                self.net.ext_grid["max_p_mw"][ID] = max_p_mw[ID]
    
    def update_polycost(self, polycost):
        """Update the polycost of each agents. \n
        Input :
            polycost (array) : array of size (n_agent, 3) representing the polynomial cost for each agent"""
        for k in range(self.n_agent):
            self.net.poly_cost.at[k,"cp1_eur_per_mw"] = polycost[k,1]
            self.net.poly_cost.at[k,"cp2_eur_per_mw2"] = polycost[k,2]
        
    def runpp(self, memory, t, grid_cost_array):
        """Run power flow and optimal flow in the network and return the results.
        Input :
            - memory (Memory class) : memory of the simulation.
            - t (int) : time of the simulation
            - grid_cost_array (array) : array of the grid cost paid by each agent (can by positive or negarive)
        return :
            - loading_percent : loading percent of each line after the powerflow
            - P_exchanged : power exchanged in the network (real power that transited)
            """
        try :
            pp.runpp(self.net, enforce_q_lims=True, algorithm="nr")
        except:
            print("PF did not converge")
        # save the network state
        loading_percent = self.net.res_line.sort_index()['loading_percent']
        P_exchanged = np.concatenate((self.net.res_ext_grid["p_mw"].to_numpy(), -self.net.res_load["p_mw"].to_numpy()))
        # Q_exchanged = np.concatenate((self.net.res_ext_grid["q_mvar"].to_numpy(), self.net.res_load["q_mvar"].to_numpy()))
        memory.line_loading_percent[t] = loading_percent
        memory.P_exchanged[t] = P_exchanged
        # memory.Q_exchanged[t] = Q_exchanged
        
        if self.compute_opf >= 1 :
            constraints  = [[self.net.line["max_loading_percent"][0], np.zeros(self.n_agent)]]
            if self.compute_opf == 2 :
                constraints.append([200, grid_cost_array])
            loading_percent_opf, P_exchanged_opf = zip(*Parallel(n_jobs=self.compute_opf)(delayed(self.run_opf)(c) for c in constraints))
            for k in range(self.compute_opf):
                memory.opf_results(loading_percent_opf[k], P_exchanged_opf[k], k, t)
        
        return loading_percent, self.net.res_ext_grid["p_mw"].to_numpy()[0]
    
    def run_opf(self, constraints):
        """Compute the OPF with the specified constraints.
        Input :
            - constraints (array) : Array of shape 2, the first argument is the line limits in %, the second the cost to be added in polycost."""
        max_loading = constraints[0]
        grid_cost = constraints[1]
        # Modify network line limits
        save_max_loading = self.net.line["max_loading_percent"] = max_loading
        self.net.line["max_loading_percent"] = max_loading
        # Modify polycost
        self.net.poly_cost.cp1_eur_per_mw += grid_cost
        try :
            pp.runopp(self.net, PDIPM_COMPTOL = 1e-12)
        except :
            print("OPF did not converge")
        # Set network how it was
        self.net.line["max_loading_percent"] = save_max_loading
        self.net.poly_cost.cp1_eur_per_mw -= grid_cost
        # Get results
        loading_percent_opf = self.net.res_line.sort_index()['loading_percent']
        P_exchanged_opf = np.concatenate((self.net.res_ext_grid["p_mw"].to_numpy(), self.net.res_gen["p_mw"].to_numpy(), -self.net.res_load["p_mw"].to_numpy()))
        # Q_exchanged_opf = np.concatenate((self.net.res_ext_grid["q_mvar"].to_numpy(), self.net.res_gen["q_mvar"].to_numpy(), self.net.res_load["q_mvar"].to_numpy()))
        return loading_percent_opf, P_exchanged_opf
    
    ########################################################################################################
    ############################################ Core functions ############################################
    ########################################################################################################
     
    def run(self, warm_start, max_it=500, SO_strategy = True, plot =False):
        """Run the simulation. \n
        Input :
            - warm_start (bool) : perform a warm start. If True the simulation start with the ADMM converged.
            - max_it (int, 500) : maximum number of itération
            - SO_strategy (True) : If True, the price can fluctuate during the warm start depending on the SO' strategy. Set False to have a fixed price.
            - plot (bool, False) : plot the convergence of the warm start
            """
        if warm_start==True:
            if SO_strategy == False :
                strategy = self.SO.strategy
                self.SO.strategy = "None" 
            self.memory_warm = self.init_memory(self.agents, self.SO, max_it)
            self.ADMM(self.memory_warm, warm_start = True, max_it=max_it)
            # Plot
            if plot ==True:
                self.memory_warm.plot_convergence(scale=True)
                self.memory_warm.plot_all_agent_power(t=max_it-1, warm=True)
                self.memory_warm.plot_agent_power_during_simu()
        
        if SO_strategy == False :
            self.SO.strategy = strategy
        self.ADMM(self.memory)
        
    def ADMM(self, memory, warm_start=False, max_it=None):
        """Apply the ADMM routine. \n
        Input :
            - memory : memory class that stores all data from the simulation
            - warm_start (bool) : Performs a warm start if True (max_it should be specified)
            - max_it (int) : only used for warm start, specifie the maximum number of iteration for the warm start.
            """
        # Init variable
        trade = np.zeros((self.n_agent, self.n_agent))
        min_p_mw = np.zeros(self.n_agent)
        max_p_mw = np.zeros(self.n_agent)
        polycost = np.zeros((self.n_agent,3))
        grid_cost_array = np.zeros(self.n_agent)
        
        # Init with warm start
        P = self.communication.get_trade()
        for k in range(len(self.agents)):
            self.agents[k].P1 = P[k,:]
        # Number of step
        if warm_start :
            n_step = max_it
        else :
            n_step = self.n_step
        # Progess bar
        pbar = tqdm(total=n_step)
        # Simulation
        for t in range(n_step):
            # Get trade and grid cost through communication
            P = self.communication.get_trade()
            grid_cost = self.communication.grid_cost
            # Each agent computes its objective power
            for k in range(len(self.agents)):
                self.agents[k].update_trade_and_price(P[:,k], grid_cost)
                trade[k], min_p_mw[k], max_p_mw[k], polycost[k], grid_cost_array[k] = self.agents[k].run(warm_start)
            memory.P[t] = trade
            self.communication.update_trade(trade)
            # Update the network and perform PF and OPF
            self.update_network(trade, min_p_mw, max_p_mw, polycost)
            loading_percent, grid = self.runpp(memory, t, grid_cost_array)
            # Compute new network cost
            grid_cost = self.SO.network_fees(loading_percent)
            memory.grid_cost[t] = grid_cost
            # Send network cost to the communication module
            self.communication.save_network_fees(grid_cost)
            self.communication.broadcast()
            pbar.update(1)
        pbar.close()