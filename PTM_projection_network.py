# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 21:52:48 2021

@author: ASUS
"""
import operator
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import pandas as pd

ptm_to_amy=[]
ptm_set=[]
amy_prot_set=[]
with open('/home/saikat/Epigenomic_proj/ptm_to_amyloid_prots.txt') as f:
    for line in f:
        ind= line.strip('\n').split('\t')
        ptm_to_amy.append((ind[0],ind[1]))
        ptm_set.append(ind[0])
        amy_prot_set.append(ind[1])
        
B= nx.Graph()

B.add_nodes_from(ptm_set, bipartite=0)
B.add_nodes_from(amy_prot_set, bipartite=1)

B.add_edges_from(ptm_to_amy)
# nx.draw(B, with_labels=1)
# plt.show()
ptm_proj= bipartite.projected_graph(B, ptm_set)
# nx.draw(ptm_proj, with_labels= 1)
# plt.show()
important_edges_ptm= nx.edge_betweenness_centrality(ptm_proj, normalized= True)
sorted_d1 = dict( sorted(important_edges_ptm.items(), key=operator.itemgetter(1),reverse=True))
# print(important_edges)

ptm_pairs=[]
with open('/home/saikat/Epigenomic_proj/edge_betweennes_ptm_projection.txt','w') as out:
    for k1,k2 in sorted_d1.keys():
        out.write("%s\t%s\t%s\n"%(k1,k2,sorted_d1[(k1,k2)]))
        ptm_pairs.append((k1,k2,sorted_d1[(k1,k2)]))
        
df_ptm_edge_betweenness=pd.DataFrame(ptm_pairs)
df_ptm_edge_betweenness.columns=["PTM1","PTM2","Edge_betweennes_weight"]

df_ptm_edge_betweenness.to_csv("/home/saikat/Epigenomic_proj/ptm_ptm_edge_betweenness.csv",sep=',',index=None,header=True)


        


        
        