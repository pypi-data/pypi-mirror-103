# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 14:46:32 2021

@author: Guenole CHEROT
"""
import numpy as np
from copy import deepcopy

class Communication():
    """
    Communication between SO and Agents. Remembers :
        - Trades between agents
        - Network cost
        
    Input :
        - n_agent (int) : number of agent in the network
        - grid_cost (float) : grid cost imposed by the SO
    
    Attribute :
        - P_buffer (array) : list of the power that each agent wants to exanche at the end of their minimization
        - P (array) : Same as P_buffer but when all agents have converged
        """
    
    def __init__(self, n_agent, grid_cost):
        self.n_agent = n_agent
        self.P = np.zeros((n_agent, n_agent))
        self.P_buffer = np.zeros((n_agent, n_agent))
        self.grid_cost = grid_cost
        self.t = 0
        
    def save_network_fees(self, grid_cost):
        """Save the network cost given by the SO. \n
        Input :
            - grid_cost (float) : network cost imposed by SO
            """
        self.grid_cost = grid_cost
    
    def update_trade(self, trade, ID=None):
        """Update the trade proposed by the agent ID. \n
        Input : 
            - trade (array) : array size (n_agent) representing the trade proposed by the agent ID.
            - ID (int) : ID of the agent proposing the trade"""
        if ID == None:
            if trade.shape == (self.n_agent, self.n_agent):
                self.P_buffer = trade
            else :
                raise ValueError("trade as not the correct shape")
        else :
            self.P_buffer[ID] = trade
        
        
    def get_trade(self, ID=None):
        """Get the trade proposed by all agent to agent number ID. \n
        Input :
            - ID (int) : ID of the agent proposing the trade. If None return the trade matrix (P)
        Output :
            - trade (array) : array size (n_agent) representing the trade proposed by all agents to agent number ID."""
        if ID == None:
            return self.P
        else :
            return self.P[:,ID]
    
    def broadcast(self):
        """Update all value of power trade (used in a synchronous algorithm)"""
        # Update the power trade
        self.P = deepcopy(self.P_buffer)
        # Increment time
        self.t += 1