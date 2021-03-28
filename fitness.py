
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 10:21:19 2021

@author: vivek
"""
###############################################################################################
# importing data and libraries#################################################################
###############################################################################################
import pandas as pd
import numpy as np
import random
import copy
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
from itertools import permutations 


df = pd.read_excel('problem1.xlsx')

###############################################################################################
# defining node and edge classes ##############################################################
###############################################################################################
class Node(object):
    def __init__(self, n, c, t, d, l):
        self.name = n
        self.cost = c
        self.time = t
        self.demand = None
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
    def __init__(self, s, d, c, t, l):
        self.source = s
        self.destination = d
        self.cost = c
        self.time = t
        self.level = l
    def getSource(self):
        return self.source
    def getDestination(self):
        return self.destination
    def getCost(self):
        return self.cost
    def getTime(self):
        return self.time
    def getLevel(self):
        return self.level
    
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
# making tdictionary containing node objects ###################################################
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
# making dictionary of edge objects#############################################################
################################################################################################
def edges(df):
    adjacency = adjacency_list(df)
    node_dict = nodes(df)
    #add level
    edge_dict = {}
    for node in adjacency:
        cost = node_dict[node].getCost()
        time = node_dict[node].getTime()  
        level = node_dict[node].getLevel()
        for neighbour in adjacency[node]:
            name = str(node)+'_'+str(neighbour)
            edge_dict[name] = Edge(node, neighbour, cost, time, level)              
    return edge_dict

################################################################################################
# returns the dictionary of random weights or a simple solution#################################
################################################################################################
def initialize_complex_map(df):    
    edges_list = edges(df)
    the_map = {}    
    for edge in edges_list:
        level = edges_list[edge].level        
        the_map[edge] = [level, random.random()]
    return the_map

################################################################################################
# returns the dictionary containing edges in different level ###################################
################################################################################################
def edge_levels(df):
    edges_list = edges(df)
    max_depth = df['relDepth'].max()
    level_list = []
    for i in range(max_depth):
        level_list.append(i+1)
    level_dict = {} 
    for i in level_list:
        level_dict[i] = []
    for edge in edges_list.values():
        level = edge.getLevel()  
        level_dict[level].append(edge)
    return level_dict

################################################################################################
# returns the total_demand #####################################################################
################################################################################################
def demand(df):
    demand = df.avgDemand.sum()
    return demand

################################################################################################
# returns dictionary containing nodes at every level############################################
################################################################################################    
def node_levels(df):
    node_dict = nodes(df)
    max_depth = df['relDepth'].max()
    level_list = []
    for i in range(max_depth+1):
        level_list.append(i)
    level_dict = {} 
    for i in level_list:
        level_dict[i] = []
    for node in node_dict.values():
        level = node.getLevel()  
        level_dict[level].append(node)
    return level_dict

################################################################################################
# returns dictionary containing names of nodes at every level###################################
################################################################################################    
def node_levels_names(df):
    node_dict = nodes(df)
    max_depth = df['relDepth'].max()
    level_list = []
    for i in range(max_depth+1):
        level_list.append(i)
    level_dict = {} 
    for i in level_list:
        level_dict[i] = []
    for node in node_dict.values():
        level = node.getLevel()  
        level_dict[level].append(node.getName())
    return level_dict

################################################################################################
# returns possible combinations at every level as a dictionary##################################
################################################################################################
def combinations_dict(df):
    node_level = node_levels(df)
    max_depth = df['relDepth'].max()
    combination_dict = {}
    for i in range(max_depth+1):
        combination_dict[i] = []   
    combination_dict[0].append(node_level[0])
    for i in range(1, max_depth+1):
        level_combinations = []
        level = node_level[i]
        for L in range(1, len(level)+1):
            for subset in itertools.combinations(level, L):
                subset = list(subset)
                level_combinations.append(subset)
                combination_dict[i] = level_combinations
    return combination_dict

################################################################################################
# returns possible combinations of names at every level as a dictionary#########################
################################################################################################
def combinations_dict_names(df):
    node_level = node_levels_names(df)
    max_depth = df['relDepth'].max()
    combination_dict = {}
    for i in range(max_depth+1):
        combination_dict[i] = []   
    combination_dict[0].append(node_level[0])
    for i in range(1, max_depth+1):
        level_combinations = []
        level = node_level[i]
        for L in range(1, len(level)+1):
            for subset in itertools.combinations(level, L):
                subset = list(subset)
                level_combinations.append(subset)
                combination_dict[i] = level_combinations
    return combination_dict


################################################################################################
# getting list of paths#########################################################################
################################################################################################
def path_list(df):
    comb_list = []
    max_depth = df['relDepth'].max()
    com = combinations_dict(df)
    arg = []
    for i in range(max_depth+1):
        arg.append(com[i])
    for j in itertools.product(*arg):
        j = list(j)

        comb_list.append(j) 
    return comb_list

################################################################################################
# getting list of dictionary of paths###########################################################
################################################################################################
def path_list_dictionary(df):
    comb_list = []
    max_depth = df['relDepth'].max()
    com = combinations_dict(df)
    arg = []
    for i in range(max_depth+1):
        arg.append(com[i])        
    for j in itertools.product(*arg):
        dic = {}
        length = len(j)-1
        for k in range(length+1):
            dic[k] = j[k]            
        comb_list.append(dic) 
    return comb_list

################################################################################################
#cerating a fitness function ###################################################################
################################################################################################
l = path_list_dictionary(df)