#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 10:21:19 2021

@author: vivek
"""
###############################################################################################
# importing data and libraries#################################################################
###############################################################################################
import random
import time
import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_excel('problem1.xlsx')
df['avgDemand'] = df['avgDemand'].fillna(0)

###############################################################################################
# defining node and edge classes ##############################################################
###############################################################################################
class Node(object):
    def __init__(self, n, c, t, d, l):
        self.name = n
        self.cost = c
        self.time = t
        self.demand = d
        self.level = l
    def getName(self):
        return self.name
    def getCost(self):
        return self.cost
    def getTime(self):
        return self.time
    def getDemand(self):
        return self.demand
    def getLevel(self):
        return self.level
    
class Edge(object):
    def __init__(self, i, n, s, d, c, t, dum):
        self.ind = i
        self.name = n
        self.source = s
        self.destination = d
        self.cost = c
        self.time = t
        self.dummy = dum
    def getInd(self):
        return self.ind
    def getName(self):
        return self.name
    def getSource(self):
        return self.source
    def getDestination(self):
        return self.destination
    def getCost(self):
        return self.cost
    def getTime(self):
        return self.time
    def getDestinationDemand(self):
        demand = self.destination.getDemand()
        return(demand)
    def getDummy(self):
        return self.dummy

###############################################################################################
# returns adjacency list ######################################################################
###############################################################################################
def adjacency_list(df):    
    max_depth = df['relDepth'].max()
    adjacency = {}
    
    for k in range(max_depth):
        level_array = []
        nextlevel_array = []
        nextlevel = k 
        level = nextlevel + 1  
    
        for i in range(len(df)):
            if df.iloc[i, 2] == level:
                name = df.iloc[i,0]
                level_array.append(name)
        for j in range(len(df)):
            if df.iloc[j, 2] == nextlevel:
                next_name= df.iloc[j,0]
                nextlevel_array.append(next_name)
        for item in level_array:
            adjacency[item] = nextlevel_array
    return adjacency
    
################################################################################################
# making dictionary containing node objects ####################################################
################################################################################################
def nodes(df):
    names = df['Stage Name'].tolist()
    cost = df['stageCost'].tolist()
    time = df['stageTime'].tolist()
    demand = df['avgDemand'].tolist()
    level = df['relDepth'].tolist()
    node_dict = {}
    for i in range(len(names)):
        name = names[i]
        node_dict[name] = Node(names[i], cost[i], time[i], demand[i], level[i])
    return node_dict
    
################################################################################################
# making dictionary of edges ###################################################################
################################################################################################
def no_dummy_edges(df):
    adjacency = adjacency_list(df)
    node_dict = nodes(df)
    edge_counter = -1 
    edge_dict = {}
    for node in adjacency:
        
        nodeObject = node_dict[node]
        cost = node_dict[node].getCost()
        time = node_dict[node].getTime()
        for neighbour in adjacency[node]:
            edge_counter = edge_counter+1            
            name = str(node)+'_'+str(neighbour)
            neighbourObject = node_dict[neighbour]
            edge_dict[name] = Edge(edge_counter, name, nodeObject, neighbourObject, cost, time)              
    return edge_dict

################################################################################################
# making dictionary of edges with dummy edges###################################################
################################################################################################
def edges(df):    
    adjacency = adjacency_list(df)
    node_dict = nodes(df)
    edge_counter = -1 
    edge_dict = {}
    for node in adjacency:
        nodeObject = node_dict[node]
        cost = node_dict[node].getCost()
        time = node_dict[node].getTime()
        for neighbour in adjacency[node]:
            edge_counter = edge_counter+1            
            name = str(node)+'_'+str(neighbour)
            neighbourObject = node_dict[neighbour]
            dummy = 0
            edge_dict[name] = Edge(edge_counter, name, nodeObject, neighbourObject, cost, time, dummy)  
    for i in node_dict:
        node = node_dict[i]
        if node.getLevel() == 0:
            n = 'dummy ' + str(node.getName())
            c = node.getCost()
            t= node.getTime()
            d = node.getDemand()
            l = -1
            dummy_node = Node(n, c, t, d, l)
            edge_counter = edge_counter + 1
            name = str(node.getName()) + ' dummy'
            source = node
            destination = dummy_node
            cost = node.getCost()
            time = node.getTime()
            dummy = 1
            edge_dict[name] = Edge(edge_counter, name, source, destination, cost, time, dummy)
    return edge_dict
    
################################################################################################
# gives adjacency dictionary of edges ##########################################################
################################################################################################
def edge_adjacency_dict(df):
    edge_dict = edges(df)    
    edge_adjacency = {}
    for i in edge_dict:
        edge = edge_dict[i]
        predecessor_list = []
        for j in edge_dict:
            predecessor = edge_dict[j]
            destination = predecessor.getDestination()
            source = edge.getSource()
            if source.getName() == destination.getName():
                predecessor_list.append(predecessor)
        edge_adjacency[edge] = predecessor_list
    return edge_adjacency

################################################################################################
# gives adjacency dictionary of indices of edges ###############################################
################################################################################################
def edge_adjacency_index_dict(df):
    edge_dict = edges(df)    
    edge_adjacency = {}
    for i in edge_dict:
        edge = edge_dict[i]
        predecessor_list = []
        for j in edge_dict:
            predecessor = edge_dict[j]
            destination = predecessor.getDestination()
            source = edge.getSource()
            if source.getName() == destination.getName():
                predecessor_list.append(predecessor.getInd())
        edge_adjacency[edge.getInd()] = predecessor_list
    return edge_adjacency

################################################################################################
# saving edge dataframes #######################################################################
################################################################################################
adjacency = edge_adjacency_dict(df)
edge_ind = edge_adjacency_index_dict(df)
edge_dict = edges(df)
node_list = nodes(df)

################################################################################################
# returns bounds of all variables ##############################################################
################################################################################################
def getBounds():
    gross_demand = 0
    bounds = []
    for i in node_list.values():
        demand = i.getDemand()
        gross_demand = gross_demand + demand
    for j in adjacency:
        bounds.append((0, gross_demand))
    return bounds   

################################################################################################
# returns  DYNAMIC bounds of all variables #####################################################
################################################################################################
def dynamic_bounds(o):
    bounds = []
    bound_dict = {}
    for i in adjacency:
        demand = i.getDestinationDemand()
        if demand != 0:
            bound_dict[i] = (0, demand)
        elif demand == 0.0:
            predecessors = adjacency[i]
            predecessor_sum = 0
            for j in predecessors: 
                flow = j.getInd()
                predecessor_sum = predecessor_sum + o[flow]
            bound_dict[i] = (0, predecessor_sum)
        if i.getDummy() == 1:
            bound_dict[i] = (0.9*demand, demand)
    for k in bound_dict.values():
        bounds.append(k)
    return bounds

################################################################################################
# returns  DYNAMIC bounds of all variables with FLOW CONSERVATION###############################
################################################################################################
def dynamic_flow_bounds(o):
    #o = [1,1,1,1,1,1,1,1,1,1,1,1]

    bounds = []
    bound_dict = {}
    total_demand = 0
    
    for i in adjacency:
        if i.getDummy() == 1:
            dem = i.getDestinationDemand()
            total_demand = total_demand + dem
        
    for i in adjacency:
        previous_flow = 0
        predecessors = adjacency[i]
        if i.getDummy() == 1:
            demand = i.getDestinationDemand()
            bound_dict[i] = (0.9*demand, demand)
        elif i.getDummy() == 0:
            if predecessors!= []:
                for j in predecessors:
                    location = j.getInd()
                    print('the predecessor of ' + i.getName() + ' at ' + str(i.getInd()) +' is ' + j.getName() + ' at ' + str(location))
                    previous_flow = previous_flow + o[location]
                bound_dict[i] = (previous_flow, previous_flow)               
            elif predecessors == []:
                bound_dict[i] = (0, total_demand)      
        
    for k in bound_dict.values():
        bounds.append(k)
    return bounds

################################################################################################
# objective function - cost of supply chain. to be minimized ###################################
################################################################################################
def objective_function(o):
    sums = 0
    penalty = 0
    for i in edge_ind:
        for j in edge_ind[i]:
            sums = sums + o[j]
        if o[i] > sums:
            penalty = penalty + 1000000
    sums2 = 0
    for i in adjacency:
        if i.getDestinationDemand() != 0:
            demand = i.getDestinationDemand()
            predecessors = adjacency[i]
            for j in predecessors:
                indices = j.getInd()
                sums2 = sums2 + o[indices]
            if sums2 > demand:
                penalty = penalty + 1000000
            if sums2 < 0.9*demand:
                penalty = penalty + 1000000
    totalcost = 0
    counter = 0
    for i in adjacency:
        counter = counter+1
        cost = i.getCost()*o[counter-1]
        totalcost = totalcost+cost            
    z = totalcost+penalty        
    return z

################################################################################################
# defining particle swarm parameters############################################################
################################################################################################       
#bounds = dynamic_bounds(o)  # upper and lower bounds of variables
nv = len(edge_ind)  # number of variables
mm = -1  # if minimization problem, mm = -1; if maximization problem, mm = 1
particle_size = 120  # number of particles
iterations = 200  # max number of iterations - 200
w = 0.8  # inertia constant
c1 = 1  # cognative constant
c2 = 2  # social constant
  
################################################################################################
# defining vizualisation parameters ############################################################
################################################################################################   
fig = plt.figure()
ax = fig.add_subplot()
fig.show()
plt.title('Evolutionary process of the objective function value')
plt.xlabel("Iteration")
plt.ylabel("Objective function")

################################################################################################
# defining particle class ######################################################################
################################################################################################ 
class Particle:
    def __init__(self):
        self.particle_position = []  # particle position
        self.particle_velocity = []  # particle velocity
        self.local_best_particle_position = []  # best position of the particle
        self.fitness_local_best_particle_position = initial_fitness  # initial objective function value of the best particle position
        self.fitness_particle_position = initial_fitness  # objective function value of the particle position
        bounds = dynamic_flow_bounds(self.particle_position)
        for i in range(nv):
            self.particle_position.append(
                random.uniform(bounds[i][0], bounds[i][1]))  # generate random initial position
            self.particle_velocity.append(random.uniform(-1, 1))  # generate random initial velocity
  
    def evaluate(self, objective_function):
        self.fitness_particle_position = objective_function(self.particle_position)
        if mm == -1:
            if self.fitness_particle_position < self.fitness_local_best_particle_position:
                self.local_best_particle_position = self.particle_position  # update the local best
                self.fitness_local_best_particle_position = self.fitness_particle_position  # update the fitness of the local best
        if mm == 1:
            if self.fitness_particle_position > self.fitness_local_best_particle_position:
                self.local_best_particle_position = self.particle_position
                self.fitness_local_best_particle_position = self.fitness_particle_position

    def update_velocity(self, global_best_particle_position):
        for i in range(nv):
            r1 = random.random()
            r2 = random.random()
  
            cognitive_velocity = c1 * r1 * (self.local_best_particle_position[i] - self.particle_position[i])
            social_velocity = c2 * r2 * (global_best_particle_position[i] - self.particle_position[i])
            self.particle_velocity[i] = w * self.particle_velocity[i] + cognitive_velocity + social_velocity
  
    def update_position(self):
        bounds = dynamic_flow_bounds(self.particle_position)
        for i in range(nv):
            self.particle_position[i] = self.particle_position[i] + self.particle_velocity[i]
            
  
            # check and repair to satisfy the upper bounds
            if self.particle_position[i] > bounds[i][1]:
                self.particle_position[i] = bounds[i][1]
            # check and repair to satisfy the lower bounds
            if self.particle_position[i] < bounds[i][0]:
                self.particle_position[i] = bounds[i][0]
  
################################################################################################
# defining optimization model class ############################################################
################################################################################################ 
class PSO:
    def __init__(self, objective_function, particle_size, iterations):
        fitness_global_best_particle_position = initial_fitness
        global_best_particle_position = []
        swarm_particle = []
        for i in range(particle_size):
            swarm_particle.append(Particle())
        A = []
        
        for i in range(iterations):
            for j in range(particle_size):
                swarm_particle[j].evaluate(objective_function)
                
                if mm == -1:
                    if swarm_particle[j].fitness_particle_position < fitness_global_best_particle_position:
                        global_best_particle_position = list(swarm_particle[j].particle_position)
                        fitness_global_best_particle_position = float(swarm_particle[j].fitness_particle_position)
                if mm == 1:
                    if swarm_particle[j].fitness_particle_position > fitness_global_best_particle_position:
                        global_best_particle_position = list(swarm_particle[j].particle_position)
                        fitness_global_best_particle_position = float(swarm_particle[j].fitness_particle_position)                
            for j in range(particle_size):
                swarm_particle[j].update_velocity(global_best_particle_position)
                swarm_particle[j].update_position()
                print('iteration ' + str(i))
                print('particle ' + str(j))
            

            A.append(fitness_global_best_particle_position)
            #Visualization
            ax.plot(A, color = 'r')
            fig.canvas.draw()
            ax.set_xlim(left = max(0, i- iterations), right = i+3)
            time.sleep(0.01)
        print('Optimal solution ', global_best_particle_position)
        print('Objective function value ', fitness_global_best_particle_position)
        plt.show()   
        
################################################################################################
# running particle swarm optimization ##########################################################
################################################################################################ 
if mm == -1:
    initial_fitness = float('inf')
if mm == 1:
    initial_fitness = -float('inf')  
PSO(objective_function, particle_size, iterations)
plt.show()
