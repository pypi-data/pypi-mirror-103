# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 14:46:32 2021

@author: Guenole CHEROT
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import statistics

class Memory():
    """Memory of all data acquired during simulation :
        - Dual update
        - Residuals
        - Power exchanged though Exogenous algo, OPF, OPF without constrains
        - Network fees (gamma)
        - network state (line rating, bus voltage)
        
    Input :
        - n_agent (int) : number of agent in the network (including the ext grid)
        - n_step (int) : number of time step
        - n_line (int) : number of line in the network
        - n_bus (int) : number of bus in the network
        - grid_cost_type (str,'uniq') : type of grid cost imposed by the SO. Can be : 'uniq', 'dist', 'zone'
        - line_limits (float) : line maximum loading in percent
        - compute_opf (int, 1) : 0 does not compute OPF, 1 compute OPF with line limits, 2 compute OPF with and without line limits
        - data (DataFrame) : times serie of the power desired by each agent
        - flex_data (DataFrame) : Flexibility of each agent
        """
    
    def __init__(self, n_agent, n_step, n_line, n_bus, grid_cost_type, line_limits, compute_opf, data, flex_data):
        self.n_agent = n_agent
        self.n_step = n_step
        self.n_line = n_line
        self.n_bus = n_bus
        
        self.grid_cost_type = grid_cost_type
        self.data = data
        self.flex_data = flex_data
        
        self.dual = np.zeros((n_step, n_agent, n_agent))
        self.P = np.zeros((n_step, n_agent, n_agent))
        self.grid_cost = np.zeros(n_step)
        self.line_limits = line_limits
        self.compute_opf = compute_opf
        self.line_loading_percent = np.zeros((n_step, n_line))
        self.P_exchanged = np.zeros((n_step, n_agent))
        # self.Q_exchanged = np.zeros((n_step, n_agent))
        
        if self.compute_opf >=1 :
            self.line_loading_percent_opf = np.zeros((n_step, n_line))
            self.P_exchanged_opf = np.zeros((n_step, n_agent))
            # self.Q_exchanged_opf = np.zeros((n_step, n_agent))
        if self.compute_opf == 2 :
            self.line_loading_percent_opf_2 = np.zeros((n_step, n_line))
            self.P_exchanged_opf_2 = np.zeros((n_step, n_agent))
            # self.Q_exchanged_opf_2 = np.zeros((n_step, n_agent))
        
        self.bus_voltage = np.zeros((n_step, n_bus))
        self.prim_res = np.zeros(n_step)
        self.dual_res = np.zeros(n_step)
        
    def opf_results(self, loading_percent_opf, P_exchanged_opf, k, t):
        """Store the OPF results.
        Input :
            - loading_percent_opf (array) : loading of each line in the network
            - P_exchanged_opf (array) : power exchanged by each agent in the network
            - k (int) : If 0, save in OPF. If 1 save in OPF without limits
            - t (int) : time of the simulation.
            """
        if k == 0 :
            self.line_loading_percent_opf[t] = loading_percent_opf
            self.P_exchanged_opf[t] = P_exchanged_opf
        if k == 1 :
            self.line_loading_percent_opf_2[t] = loading_percent_opf
            self.P_exchanged_opf_2[t] = P_exchanged_opf
        
    def compute_residual(self):
        """Compute the residuals"""
        for k in range(self.n_step):
            self.prim_res[k] = np.sum(np.sum(np.square(self.P[k] + self.P[k].T), axis=1))
            self.dual_res[k] = np.sum(np.sum(np.square(self.P[k] - self.P[k-1]), axis=1))
        self.prim_res[0] = self.prim_res[1]
        self.dual_res[0] = self.dual_res[1]
        return self.prim_res, self.dual_res

    ######################################################################################################
    ############################################### Stats ################################################
    ######################################################################################################
    
    def stats_power(self):
        """Return the median and last 5% decile of the difference between the power exchanged trough the exogenous algo and the OPF for each agent."""
        if self.compute_opf == 0:
            raise ValueError("OPF as not been computed during simulation. compute_opf = 0.")
        Delta_P = 100*np.sum(np.abs(self.P_exchanged - self.P_exchanged_opf), axis=0)/np.sum(np.abs(self.P_exchanged_opf), axis=0)
        q = statistics.quantiles(Delta_P, n = 20)
        median = q[9]
        last_5_percent = q[-1]
        return median, last_5_percent
    
    def stats_lines(self, compare_opf=False):
        """Return the median and last 5% decile of the line overloading. Difference between exogenous algo and line limits for every time step.
        Input :
            - compare_opf (bool, False) : if True the line loading will be compared with the opf. With self.line_limits otherwise."""
        l = np.max(self.line_loading_percent, axis=1)
        if compare_opf:
            if self.compute_opf == 0:
                raise ValueError("OPF as not been computed during simulation. compute_opf = 0.")
            l_opf = np.max(self.line_loading_percent_opf, axis=1)
            overload = l-l_opf
        else :
            overload = l-self.line_limits
        overload[overload<0] = 0
        q = statistics.quantiles(overload, n = 20)
        median = q[9]
        last_5_percent = q[-1]
        return median, last_5_percent
        
    ######################################################################################################
    ################################################ PLOT ################################################
    ######################################################################################################
    
    def plot_convergence(self, scale = False, ax=None, title=False):
        """Plot evolution of the primal and dual residual depending on the number of iteration. \n
        Input :
            - scale (bool, False) : Set to True to plot : (primal_residual/sum(Power^2)).
            - ax (plt ax, None) : matplotlib pyplot ax on wich to plot
            - title (bool, False) : print figure's title if True"""
        plot = False
        if ax == None:
            plot = True
            fig, ax = plt.subplots(figsize=(6.4, 2.5), dpi=300)
        
        prim, dual = self.compute_residual()
        if scale :
            scale_factor = np.sum(np.sum(np.square(self.P), axis=1), axis=1)
            label = "(in %)"
            # Divide by 100 because the result is in %
            prim /= scale_factor/100
            dual /= scale_factor/100
        else :
            label = ""
        ax.semilogy(prim, label="Primal residual")
        ax.semilogy(dual, label="Dual residual")
        ax.grid()
        ax.legend()
        if title:
            ax.set_title("Evolution of residuals troughout the simulation")
        ax.set_xlabel("Time (min)")
        ax.set_ylabel("Residual " + label)
        ax.set_xlim((0,self.n_step))
        if plot :
            plt.show()
        
    def plot_agent_power_during_simu(self, list_agent=None, legend=False, ax=None, title=False):
        """Plot the power calculated by each agent by the algorithm throughout the simulation.
        Input :
            - list_agent (array) : list of agent ID to be ploted.
            - legend (bool) : If True, display the legend
            - ax (plt ax, None) : matplotlib pyplot ax on wich to plot
            - title (bool, False) : print figure's title if True
        """
        plot = False
        if ax == None:
            plot = True
            fig, ax = plt.subplots()
        
        if list_agent is not None :
            for k in list_agent :
                ax.plot(np.sum(self.P[:,k,:],axis=1), label="agent {0}".format(k))
        else :
            for k in range(self.n_agent):
                ax.plot(np.sum(self.P[:,k,:],axis=1), label="agent {0}".format(k))
        if legend == True :
            ax.legend()
        ax.grid()
        if title:
            ax.set_title("Power computed during the simulation")
        ax.set_xlabel("time (min)")
        ax.set_ylabel("Power (MW)")
        ax.set_xlim((0,self.n_step))
        if plot :
            plt.show()
        
    def plot_compare_to_OPF_simu(self, ID_agent, legend=False, objective=False, ax=None, title=False):
        """Plot the power calculated by agent "ID_agent" troughout the simulation.
        Input :
            - ID_agent : agent ID to be ploted.
            - legend (bool) : If True, display the legend
            - objective (bool) : If True, display the objective power
            - ax (plt ax, None) : matplotlib pyplot ax on wich to plot
            - title (bool, False) : print figure's title if True
        """
        plot = False
        name = ["(a) ", "(b) ", "(c) ", "(d) "]
        if ax == None:
            plot = True
            name = ["","","",""]
            fig, ax = plt.subplots()
        
        ex, = ax.plot(1e3*self.P_exchanged[:,ID_agent], label="{0}Exogenous".format(name[0]))
        
        if self.compute_opf >= 1:
            opf, = ax.plot(1e3*self.P_exchanged_opf[:,ID_agent], color='orange', label="{0}OPF".format(name[2]))
        if self.compute_opf == 2:
            opf_2, = ax.plot(1e3*self.P_exchanged_opf_2[:,ID_agent],'--', color='xkcd:orange', label="{0}OPF without line limits".format(name[3]))
        
        if objective :
            p = self.data[self.data["dataid"]==ID_agent].sort_values(by='time').grid.values
            obj, = ax.plot(p, '--g', label="{0}Objective".format(name[1]))

        if legend == True :
            ax.legend()
        ax.grid()
        if title:
            ax.set_title("Power produced during the simulation, f={0}".format(np.round(self.flex_data.flexibility[ID_agent],0)))
        ax.set_xlabel("time (min)")
        ax.set_ylabel("Power (kW)")
        ax.set_xlim((0,self.n_step))
        
        ax.text(0.05, 0.15, "Agent {0}".format(ID_agent), transform=ax.transAxes,
                fontsize=10, verticalalignment='top')
        
        if plot :
            plt.show()
        else :
            if self.compute_opf == 2:
                return ex, obj, opf, opf_2
            else :
                raise ValueError("compute_opf = 2 mandatory")
            
    def plot_line_loading(self, t, ax=None, title=False):
        """Plot the line loading resulting from the load flow.\n
        Input :
            - t (int) : time of the simulation.
            - ax (plt ax, None) : matplotlib pyplot ax on wich to plot
            - title (bool, False) : print figure's title if True
        """
        plot = False
        if ax == None:
            plot = True
            fig, ax = plt.subplots()
        M = np.linspace(0,self.n_line-1,self.n_line)
        ax.bar(M, height=self.line_loading_percent[t], bottom=0)
        ax.set_ylim((0,200))
        ax.set_xlim((-.5,self.n_agent+0.5))
        ax.plot(M, 100*np.ones(len(M)), 'g--')
        if title:
            ax.set_title("loading percent of every line")
        ax.set_xlabel("Line n")
        ax.set_ylabel("Loading (%)")
        ax.grid()
        if plot :
            plt.show()
            

    def plot_cost_evolution(self, ax=None, title=False):
        """Plot the evolution of the cost during one simulation. \n
        Input :
            - ax (plt ax, None) : matplotlib pyplot ax on wich to plot
            - title (bool, False) : print figure's title if True"""
        plot = False
        if ax == None:
            plot = True
            fig, ax = plt.subplots()
        
        T = np.linspace(0,self.n_step-1,self.n_step)
        if self.grid_cost_type == "uniq":
            ax.plot(T, 60*self.grid_cost, color="black") # We multiply by 60 to have the price in €/MWh and not €/MWmin
            if title:
                ax.set_title("Evolution of the cost during the simulation")
            ax.set_xlabel("time (min)")
            ax.set_ylabel("Grid cost (€/MWh)")
            ax.set_xlim((0,self.n_step))
            ax.grid()
            if plot :
                plt.show()
        else :
            raise ValueError("Not implemented yet")

    def plot_max_loading_percent(self, ax=None, title=False):
        """Plot the maximum loading percent during a simulaiton. \n
        Input :
            - ax (plt ax, None) : matplotlib pyplot ax on wich to plot
            - title (bool, False) : print figure's title if True
        """
        plot = False
        if ax == None:
            plot = True
            fig, ax = plt.subplots()
        
        l = np.max(self.line_loading_percent, axis=1)
        T = np.linspace(0,self.n_step-1,self.n_step)
        ax.plot(T, l, label="Exogenous")
        
        if self.compute_opf >= 1:
            l_opf = np.max(self.line_loading_percent_opf, axis=1)
            ax.plot(T, l_opf,color='orange', label="OPF")
            
        if self.compute_opf == 2:
            l_opf_2 = np.max(self.line_loading_percent_opf_2, axis=1)
            ax.plot(T, l_opf_2,'--',color='xkcd:orange', label="OPF without line limits")
        
        if title:
            ax.set_title("Evolution of the maximum loading during the simulation")
        ax.set_xlabel("time (min)")
        ax.set_ylabel("Maximum loading of the lines (in %)")
        ax.set_xlim((0,self.n_step))
        # ax.set_ylim(55,81)
        ax.legend()
        ax.grid()
        if plot :
            plt.show()
        
    def plot_all_agent_power(self, t, warm=False, ax=None, title=False):
        """Plot the power exchanged with the exogenous algorithm and with the OPF at time t.
        Input :
            - t (int) : time slot to visualise.
            - warm (bool) : If True plot the result of the warm start.
            - ax (plt ax, None) : matplotlib pyplot ax on wich to plot
            - title (bool, False) : print figure's title if True"""
        if warm :
            desired = 1e-3*self.data[self.data["time"]==0].sort_values(by='dataid')["grid"].values
        else :
            desired = 1e-3*self.data[self.data["time"]==t].sort_values(by='dataid')["grid"].values
        # Power computed by the power flow
        exchanged = np.copy(self.P_exchanged[t])
        if self.compute_opf >= 1 :
            # Power computed by the OPTIMAL power flow
            exchanged_opf = np.copy(self.P_exchanged_opf[t])
        
        x = np.arange(self.n_agent)  # the label locations
        width = 0.2  # the width of the bars
        
        plot = False
        if ax == None:
            plot = True
            fig, ax = plt.subplots()
        rects1 = ax.bar(x - width, desired, width, label="P desired")
        rects2 = ax.bar(x, exchanged, width, label="P exogenous")
        if self.compute_opf >= 1 :
            rects3 = ax.bar(x + width, exchanged_opf, width, label ="P OPF")
        ax.set_ylabel('Power consumed (MW)')
        ax.set_xlabel("agents number")
        if title:
            ax.set_title("Power exchanged by each agent at time step {0}".format(t))
        ax.set_xticks(x)
        ax.legend()
        if plot :
            plt.show()
        
    def plot_cost_objective_function(self, t, verbose=False, ax=None, title=False):
        """Compute the grid cost paid by each agent at t. \n
        Input :
            - t (int) : time of the simulation
            - verbose (bool, True) : return total cost if True
            - ax (plt ax, None) : matplotlib pyplot ax on wich to plot
            - title (bool, False) : print figure's title if True"""
        plot = False
        if ax == None:
            plot = True
            fig, ax = plt.subplots()
        
        p = 1e-3*self.data[self.data["time"]==t].sort_values(by='dataid')["grid"].values
        res_p = np.copy(self.P_exchanged[t])
        f = self.flex_data.flexibility
        a = f*p*p
        b = -2*f*p
        
        cost = a + b*res_p + f*res_p*res_p
        cost_tot = np.sum(cost)
        
        # PLOT
        M = np.linspace(0,self.n_agent-1,self.n_agent)
        ax.bar(M, height=cost, bottom=0)
        ax.set_xlim((-.5,self.n_agent+0.5))
        if title:
            ax.set_title("Cost suffered by each agent a time {0}".format(t))
        ax.set_xlabel("Agent n")
        ax.set_ylabel("cost objective function")
        ax.grid()
        if plot :
            plt.show()
        if verbose :
            return (cost_tot)
    
    def plot_flexibility(self, ax=None, title=False):
        """Compute the total cost t the end of the simulation. \n
        Input :
            - ax (plt ax, None) : matplotlib pyplot ax on wich to plot
            - title (bool, False) : print figure's title if True"""
        plot = False
        if ax == None:
            plot = True
            fig, ax = plt.subplots()
        
        M = np.linspace(0,self.n_agent-1,self.n_agent)
        ax.bar(M, height=self.flex_data.flexibility, bottom=0)
        ax.set_xlim((-.5,self.n_agent+0.5))
        if title:
            ax.set_title("Flexibility of each agent")
        ax.set_xlabel("Agent n")
        ax.set_ylabel("Flexibility")
        ax.grid()
        if plot :
            plt.show()
    
    def plot_fig1(self, ID_not_flex, ID_flex, title=False):
        """Plot the first fgure in the article ISGT.
        Input :
            - ID_not_flex (int) : ID of a non flexible agent.
            - ID_flex (int) : ID of a flexible agent.
            - title (bool, False) : print figure's title if True"""
        if self.compute_opf != 2:
            print("Can't plot fig, compute_opf needs to be egals to 2.")
            return(self.compute_opf)
        fig = plt.figure(figsize=(8,0.8*8), dpi=600)
        gs = fig.add_gridspec(4, hspace=0)
        axs = gs.subplots(sharex=True)
        ex, obj, opf, opf_2 = self.plot_compare_to_OPF_simu(ID_agent=ID_not_flex, legend=False, objective=True, ax=axs[0])
        self.plot_compare_to_OPF_simu(ID_agent=ID_flex, legend=False, objective=True, ax=axs[1])
        self.plot_max_loading_percent(ax=axs[2])
        self.plot_cost_evolution(ax=axs[3])
        # # Common y axis for the 2 first plot
        # axs[0].sharey(axs[1])
        # legend for the 3 firts pots
        first_legend = axs[0].legend(handles=[ex, obj], loc=(0.36, -0.2), framealpha=1)
        axs[0].set_zorder(1)
        axs[0].set_xlabel("")
        # Add the legend manually to the current Axes.
        axs[0].add_artist(first_legend)
        # Create another legend for the second line.
        axs[0].legend(handles=[opf, opf_2], loc=(0.62, -0.2), framealpha=1)
        axs[2].get_legend().remove()
        
        # Delete y label and title
        for k in range(4):
            axs[k].set_title("")
            axs[k].set_ylabel("")
            
        if title:
            fig.suptitle('Evolution of the power, cost and line loading during one simulation', fontsize=14, x=0.5,y = 0.93)
        # ylabel
        x = 0.04
        fig.text(x+0.01, 0.79, 'Power (kW)', va='center', rotation='vertical')
        fig.text(x+0.01, 0.6, 'Power (kW)', va='center', rotation='vertical')
        fig.text(x, 0.42, 'Max line \n loading (%)', va='center', rotation='vertical')
        fig.text(x, 0.2, 'Cost \n (€/MWh)', va='center', rotation='vertical')

        plt.show()
        
    def plot_cost_vs_flex(self, ID_not_flex=None, ID_flex=None, ax=None, title=False):
        """Plot the grid cost paid by each agent as a function of their fllexibility. \n
        Input :
            - ID_not_flex (int, None) : ID of an unflexible agent. Default is None, not plotted.
            - ID_flex (int, None) : ID of a flexible agent. Default is None, not plotted.
            - ax (plt ax, None) : matplotlib pyplot ax on wich to plot
            - title (bool, False) : print figure's title if True"""
        plot = False
        if ax == None:
            plot = True
            fig, ax = plt.subplots(figsize=(6.4, 2.5), dpi=300)
        
        exchanged = np.abs(self.P_exchanged)
        cost = np.matmul(self.grid_cost,exchanged)
            
        cost = np.divide(cost,np.sum(exchanged, axis=0)/60)
        ax.plot(self.flex_data.flexibility[1:], cost[1:], "o")
        if title:
            ax.set_title("Grid cost paid function of flexibility")
        ax.set_ylabel("Grid cost paid (€/MWh)")
        ax.set_xlabel("Flexibility")
        ax.grid()
        
        # Spot specific agent
        if ID_not_flex != None :
            x, y = (self.flex_data.flexibility[ID_not_flex], cost[ID_not_flex])
            ax.annotate('Agent {0}'.format(ID_not_flex), xy=(x, y),  xycoords='data',
                xytext=(x-10, y-6), textcoords='data',
                arrowprops=dict(facecolor='green', shrink=0.05),
                horizontalalignment='right', verticalalignment='top')
            
        if ID_flex != None :
            x, y = (self.flex_data.flexibility[ID_flex], cost[ID_flex])
            ax.annotate('Agent {0}'.format(ID_flex), xy=(x, y),  xycoords='data',
                xytext=(x+50, y-4), textcoords='data',
                arrowprops=dict(facecolor='green', shrink=0.05),
                horizontalalignment='right', verticalalignment='top')
            
        if plot:
            plt.show()
            
    def plot_overload_histogram(self, ax=None, title=False):
        """Plot histogram of all line overload throughtout the simulation. \n
        Input :
            - ax (plt ax, None) : matplotlib pyplot ax on wich to plot
            - title (bool, False) : print figure's title if True"""
        plot = False
        if ax == None:
            plot = True
            fig, ax = plt.subplots(figsize=(6.4, 2.1), dpi=300)
        
        m1 = self.line_loading_percent.max()
        m2 = self.line_loading_percent_opf_2.max()
        m = max(m1,m2)
        bins = np.linspace(0,int(m)+1,int(m)+2)
        n,_,_ = ax.hist(self.line_loading_percent.flatten(), bins=bins, label="Exogenous")
        n2,_,_ = ax.hist(self.line_loading_percent_opf_2.flatten(), label="OPF without constrains", bins=bins, alpha=0.5, zorder=0)#, histtype=u'step', linewidth=1)
        oc = max(n)
        ax.plot([self.line_limits,self.line_limits], [0, oc*1.02], '--g')
        if title:
            ax.set_title("Histogram of the overload")
        ax.set_ylabel("Number of occurence")
        ax.set_xlabel("Line loading (%)")
        ax.set_xlim((0,int(m)+1))
        # ax.set_ylim((0,oc*1.02))
        ax.set_yscale('log', nonposy='clip')
        ax.legend(framealpha=1)
        ax.grid()
        
        ax.annotate('maximum  \n line loading', xy=(self.line_limits, oc/20),  xycoords='data',
            xytext=(self.line_limits*0.83, oc/2), textcoords='data',
            arrowprops=dict(facecolor='green', shrink=0.05),
            horizontalalignment='right', verticalalignment='top')
            
        if plot:
            plt.show()
        print(round(100*np.sum(n[100:])/np.sum(n),1),"% above 100%.")
        print("Maximum loading = ", np.size(n), "%")
            
    def PI_sensi_analysis(self, Stats_power, Stats_lines, Kp, Ki, custom_label = False, title=False):
        """Plot the sensivity analysis for the PI controller.
        Input :
            - Stats_power (array) : Array of shape (n_Kp, n_Ki, 2) representing the median and last decile for the power exchange during the simulation.
            - Stats_lines (array) : Array of shape (n_Kp, n_Ki, 2) representing the median and last decile for the line overloading during the simulation.
            - Kp (array) : Kp (proportional gain) array used to compute Stat_power and Stat_lines.
            - Ki (array) : Ki (integral gain) array used to compute Stat_power and Stat_lines.
            - custom_label (bool, False) : Set the custom label if true. Automatic otherwise.
            - ax (plt ax, None) : matplotlib pyplot ax on wich to plot.
            - title (bool, False) : print figure's title if True.
            """
        fig, axs = plt.subplots(2, 2, figsize=(7, 7), dpi=300, sharex=True, sharey=True)
        if title:
            fig.suptitle('PI sensivity analysis')
        
        Stats_lines[Stats_lines==0] = 0.001
        
        images = []
        for i in range(2):
            for j in range(2):
                if i == 0 :
                    data = Stats_power[:,:,j]
                else :
                    data = Stats_lines[:,:,j]
                images.append(axs[i, j].imshow(data, origin="lower"))
                axs[i, j].label_outer()
        
        # Set title
        axs[0, 0].set_title('(a) Median power not delived')
        axs[0, 1].set_title('(b) 95% quantile \n power not delived')
        axs[1, 0].set_title('(c) Median overflow')
        axs[1, 1].set_title('(d) 95% quantile overflow')
        
        # Set axis label
        if custom_label :
            axs[0, 0].set_xticks([0,1,7,13])
            axs[0, 0].set_yticks([0,1,5,9])
            axs[0, 0].set_xticklabels(["0", "1e-3", "0.01", "0,1"])
            axs[0, 0].set_yticklabels(["0", "0.001", "0.01", "0,1"])
        else :
            axs[0, 0].set_xticks(np.arange(len(Ki)))
            axs[0, 0].set_yticks(np.arange(len(Kp)))
            axs[0, 0].set_xticklabels(Ki)
            axs[0, 0].set_yticklabels(Kp)
    
        axs[0,0].set(xlabel='', ylabel='Kp')
        axs[0,1].set(xlabel='', ylabel='')
        axs[1,0].set(xlabel='Ki', ylabel='Kp')
        axs[1,1].set(xlabel='Ki', ylabel='')
            
        # Find the min and max of all colors for use in setting the color scale.
        vmin = 1 #min(np.min(Stats_power),np.min(Stats_lines))
        vmax = max(np.max(Stats_power),np.max(Stats_lines))
        norm = colors.LogNorm(vmin=vmin, vmax=vmax)
        for im in images:
            im.set_norm(norm)
        
        # Change position of the plots
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.05, hspace=0)
        x,y,w,h = axs[0,0].get_position().bounds
        axs[0,0].set_position([x,y-0.05,w,h])
        x,y,w,h = axs[0,1].get_position().bounds
        axs[0,1].set_position([x,y-0.05,w,h])
        # fig.tight_layout()
        
        cax = plt.axes([0.1, +0.05, 0.8, 0.04])
        cbar = fig.colorbar(images[0],cax=cax, orientation='horizontal', ticks=[1,5, 10, 20])
        cbar.ax.set_xticklabels(['<1%','5%', '10%', '20%'])
        plt.show()
        