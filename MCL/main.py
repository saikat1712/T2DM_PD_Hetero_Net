# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 12:12:12 2018

@author: SAIKAT BISWAS
"""

import numpy 
import Graph
import Markov_clustering as mc
import networkx as nx

f=open('all_PPI.txt','r')

G = nx.Graph()
 
grafo = Graph.Graph()
for line in f:
    edges = line.split()
    if(line!='\n'):
        G.add_edge(edges[0], edges[1])
        grafo.addNode(edges[0], edges[0])
        grafo.addNode(edges[1], edges[1])
        grafo.addEdge(edges[0], edges[1])

matrix, mapBackToKeys = grafo.getGraphMatrix()
numpymat = numpy.array(matrix)

result = mc.run_mcl(numpymat)           # run MCL with default parameters
clusters = mc.get_clusters(result)    # get the clusters


for i in range(len(clusters)):    
     with open("cluster%s.txt" %i,'w') as f:         
        for x in clusters[i]:
            f.write(mapBackToKeys[x]+'\n')

print("completed")
