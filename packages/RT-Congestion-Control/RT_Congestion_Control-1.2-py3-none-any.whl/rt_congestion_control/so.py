# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 15:49:33 2020

@author: Guenole CHEROT
"""

class SO():
    """System Operator of the network.
    He is able to change the price of each transaction in order to change agents consumption and line loading percent. \n
    Input :
        - n_agent (int) : number of agent in the network
        - grid_cost (float) : unit cost used be the SO the regulate the market (only used when "strategy == None")
        - strategy (str, "None") : tarification strategy. Can be : "None", "PI"
        - Kp (float, 1) : proportional gain for the correction of the price (see self.PI_tarification)
        - Ki (float, 1) : integral gain for the correction of the price (see self.PI_tarification)
        - Kd (float, 1) : proportionnal gain for the correction of the price (see self.PI_tarification)
        - Ts (float, 1) : Sample time for the correction of the price (see self.PI_tarification)
        - line_limits (float, 40) : line maximum loading in percent.
        - grid_cost_type (str,'uniq') : type of grid cost imposed by the SO. Can be : 'uniq', 'zone'
    """
    
    ########################################################################################################
    ########################################### INIT and  SETERS ###########################################
    ########################################################################################################
    
    def __init__(self, n_agent, grid_cost, strategy="None", Kp=1, Ki=1, Kd=0, Ts=1, line_limits=40, grid_cost_type="uniq"):
        self.n_agent = n_agent
        if strategy=="None":
            self.grid_cost = grid_cost
        else :
            self.grid_cost = 0
        self.strategy = strategy
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.Ts = Ts
        self.line_limits = line_limits
        self.grid_cost_type = grid_cost_type
        # time
        self.t = 0
        self.margin_sum = 0
        
        # Used in the PID controler (memory of the margin)
        self.margin_1, self.margin_2 = 0, 0
        self.cost_1 = None
        self.cost = 0
        
        
    ########################################################################################################
    ############################################ SET NETWORK COST ##########################################
    ########################################################################################################
    
    def network_fees(self, loading_percent):
        """
        Input :
            - loading_percent (array) : array of size (n_line) representing each line overload"""
        # Update price
        self.grid_cost = self.proposed_cost(loading_percent)
        self.t+=1
        return self.grid_cost
        
    def proposed_cost(self, line_loading_percent):
        """Cost proposed by the SO inder to change the total amount of energy exchanged in the system. \n
        Input :
            - line_loading_percent (array) : Vector of size (n_line) representing the loading percent of each line.
        Output :
            - cost (float) : new cost"""
        # The first idea is to rise the price if the line loading are above 100% (We could also implement a PID or something like that)
        if self.strategy == "None" :
            cost = self.grid_cost
        elif self.strategy == "PI":
            cost = self.PI_tarification(line_loading_percent)
        else :
            raise ValueError("The tarification {0} does not exist.".format(self.strategy))
        return cost
    
    def PI_tarification(self, line_loading_percent):
        """Compute the the price with a PID controler. The control variable is the maximum loading percent of all lines in the network.
        Input :
            - line_loading_percent : Loading of each line in percent."""
        # Constants for the PID
        a = self.Kp + self.Ki*self.Ts/2 + self.Kd/self.Ts
        b = -self.Kp + self.Ki*self.Ts/2 - 2*self.Kd/self.Ts
        c = self.Kd/self.Ts
        
        self.margin = max(line_loading_percent) - self.line_limits
        if self.cost <= 0:
            self.margin = max(0, self.margin)
        
        if self.cost_1 == None : #This mean this is the first iteration
            self.cost = self.Kp*self.margin + self.Ki*self.Ts*self.margin + (self.Kd/self.Ts)*(self.margin - self.margin_1)
            self.cost_1 = self.cost
            return max(0,self.cost)
        
        if self.t%1 == 0:
            self.cost = self.cost_1 + a*self.margin + b*self.margin_1 + c*self.margin_2
            self.margin_1, self.margin_2 = self.margin, self.margin_1
            self.cost_1 = self.cost
            return max(0,self.cost)
        else :
            return max(0,self.cost)
        
    ########################################################################################################
    ################################################ INFO SO ###############################################
    ########################################################################################################
    
    def __repr__(self):
        """Give usefull information about agent n."""
        # General info
        ret = "Kp : " + str(self.Kp) +"\n"
        ret += "Ki : " + str(self.Ki)+"\n"
        ret += "Kd : " + str(self.Kd)+"\n"
        ret += "Ts : " + str(self.Ts)+"\n"
        ret += "Line limits : " + str(self.line_limits)
        return ret