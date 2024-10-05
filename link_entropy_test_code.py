#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 11:37:07 2021

@author: saikat
"""

import h5py
import numpy as np
from tempfile import mkdtemp
import os.path as path
from math import log2
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.decomposition import NMF
from scipy.stats import entropy
import pandas as pd
from sqlitedict import SqliteDict
#from scipy.special import kl_div
from sklearn.preprocessing import normalize

g=nx.Graph()
g.add_edge(1,4)
g.add_edge(1,3)
g.add_edge(1,2)
g.add_edge(2,3)
g.add_edge(4,6)
g.add_edge(4,5)
g.add_edge(5,6)
g.add_edge(5,8)
g.add_edge(5,7)
g.add_edge(7,8)
g.add_edge(7,9)
g.add_edge(9,8)
nx.draw(g, with_labels = True)
plt.savefig("filename.png")

nodelist=sorted(list(g.nodes))
edgelist_arr=np.array(g.edges)
filename = path.join(mkdtemp(), 'newfile.dat') ## writing large array in disk
edgelist = np.memmap(filename, dtype='int64', mode='w+', shape=edgelist_arr.shape)
edgelist[:]=edgelist_arr[:]
edgelist=np.sort(edgelist)
edge_df=pd.DataFrame(edgelist,columns=['node1','node2'])

with h5py.File('file.h5','w') as hf:
    hf.create_dataset('file',data= nx.to_numpy_matrix(g,nodelist))

with h5py.File('file.h5','r') as hf:
    data_arr=hf['file'][:]
    # X_norm=normalize(data_arr) 
    # model = NMF(n_components=2, init='random', random_state=0)
    model = NMF(n_components=2, init='nndsvda', solver='mu')
    W = model.fit_transform(data_arr)
    H = model.components_
    # W=normalize(W)
    ## creating dict of information entropy of nodes
    j=0
    d_entropy=SqliteDict("./my_db.sqlite",autocommit=True) ##Handling large data with dictionary
    for i in range(len(W)):
        j=i+1
        p= entropy(W[i],base=2)
        d_entropy[j]=p
        
    df_entropy_r1= pd.DataFrame(d_entropy.items(),columns=['node1', 'entropy_n1'])
    df_entropy_r2= pd.DataFrame(d_entropy.items(),columns=['node2', 'entropy_n2'])
    df_entropy_r1['node1']=df_entropy_r1['node1'].astype(int)
    df_entropy_r2['node2']=df_entropy_r2['node2'].astype(int)
    
    ## Merging the entropy dictionary with the edge dataframe
    edge_df=pd.merge(edge_df,df_entropy_r1,how='inner',on=['node1'])
    edge_df=pd.merge(edge_df,df_entropy_r2,how='inner',on=['node2'])
    ## iterating over dictionary and updating edge_df dataframe
    
    edge_df['n1_n2_avg']=edge_df[['entropy_n1', 'entropy_n2']].mean(axis=1)
    edge_arr=edge_df.to_numpy()
    edge_df.to_csv("edge_entropy.csv",index=None)
    
    ## iterating over edges
    
    def log_val(a,b):
        if a>0.0:
            try: return log2(a/b)
            except ZeroDivisionError: return 0.0
        else:
            return 0.0
        
    def kl_divergence(m1,m2):
        return sum(m1[j]*log_val(m1[j],m2[j]) for j in range(len(m1)))
    
    # calculate the jensen-shannon divergence
    def jensenshannon(n1,n2,W):
        ind1=n1-1
        ind2=n2-1
        m=0.5 * (W[ind1]+W[ind2])
        res= 0.5 * kl_divergence(W[ind1],m) + 0.5 * kl_divergence(W[ind2],m)
        return res
    
    
    with open("test_link_text.txt",'w') as out:
        for k1 in range(len(edge_arr)):
            js_div=jensenshannon(int(edge_arr[k1][0]),int(edge_arr[k1][1]),W)
            le= 0.5 * (edge_arr[k1][4] + js_div)
            out.write("%d\t%d\t%s\n"%(int(edge_arr[k1][0]),int(edge_arr[k1][1]),le))
            
    weighted_df=pd.read_csv("test_link_text.txt",sep='\t',header=None)
    weighted_df.columns=['entity1','entity2','link_weight']
    weighted_df.to_csv("test_link.csv",index=None)
    d_entropy.close()
    
hf.close()

# with open("test_link_text.txt",'w') as out:
#     for k in range(len(edgelist)):
#         for a1 in d_entropy.keys():
#             if edgelist[k][0]==d_entropy[a1][1]:
#                 v1= d_entropy[a1][0]
#                 e1=a1
#             else:
#                 pass
#             if edgelist[k][1]==d_entropy[a1][1]:
#                 v2= d_entropy[a1][0]
#                 e2=a1
#             else:
#                 pass
#         # edge_ent[(e1,e2)]=[v1,v2]
#         js_div=jensenshannon(edgelist[k][0],edgelist[k][1],W)
#         le= 0.5 * (float((v1 + v2)/2) + js_div)
#         # LE_entropy['le'+''.join([str(edgelist[k][0]),str(edgelist[k][1])])]= le
#         # LE_entropy_list.append((edgelist[k][0],edgelist[k][1],le))
#         out.write("%s\t%s\t%s\n"%(edgelist[k][0],edgelist[k][1],le))
    

    
    
