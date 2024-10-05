#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 22:01:09 2021

@author: saikat
"""

import h5py
import numpy as np
from tempfile import mkdtemp
import os.path as path
from math import log2
import networkx as nx
#import matplotlib.pyplot as plt
from sklearn.decomposition import NMF
from scipy.stats import entropy
import pandas as pd
from sqlitedict import SqliteDict
from sklearn.preprocessing import normalize

network_df= pd.read_csv("/localhome/pabitra/PD_network/PD_final_entity_id_map_hetero_net.csv")

hetero_net=network_df[['entity1','entity2']]

hetero_net=hetero_net.sort_values(by=['entity1','entity2'])
hetero_net['weight']=1.0

vals=np.unique(hetero_net[['entity1','entity2']])
hetero_net_final=pd.DataFrame(0, index=vals, columns=vals)
f=hetero_net_final.index.get_indexer
hetero_net_final.values[f(hetero_net.entity1),f(hetero_net.entity2)] = hetero_net.weight.values

G=nx.Graph()
G=nx.from_pandas_adjacency(hetero_net_final,create_using=G)

nodelist=sorted(list(G.nodes))
edgelist_arr=np.array(G.edges)
#filename = path.join(mkdtemp(), 'newfile_PD.dat') ## writing large array in disk
#edgelist = np.memmap(filename, dtype='int64', mode='w+', shape=edgelist_arr.shape)
#edgelist[:]=edgelist_arr[:]

edgelist=edgelist_arr

edgelist=np.sort(edgelist)
edge_df=pd.DataFrame(edgelist,columns=['node1','node2'])

with h5py.File('file_PD_mat.h5','w') as hf:
    hf.create_dataset('file_PD_mat',data=nx.to_numpy_matrix(G,nodelist))

with h5py.File('file_PD_mat.h5','r') as hf:
    data_arr=hf['file_PD_mat'][:]
    X_norm=normalize(data_arr) 
    model = NMF(n_components=2, init='nndsvda', solver='mu')
    W = model.fit_transform(X_norm)
    H = model.components_
    
    ### creating dict of information entropy of nodes
    
    d_entropy=SqliteDict("./my_db.sqlite",autocommit=True) ##Handling large data with dictionary
    for i in range(len(W)):
        p= entropy(W[i],base=2)
        d_entropy[i]=p
        
    df_entropy_r1= pd.DataFrame(d_entropy.items(),columns=['node1', 'entropy_n1'])
    df_entropy_r2= pd.DataFrame(d_entropy.items(),columns=['node2', 'entropy_n2'])
    df_entropy_r1['node1']=df_entropy_r1['node1'].astype(int)
    df_entropy_r2['node2']=df_entropy_r2['node2'].astype(int)
    
    
    ## Merging the entropy dictionary with the edge dataframe
    edge_df=pd.merge(edge_df,df_entropy_r1,how='inner',on=['node1'])
    edge_df=pd.merge(edge_df,df_entropy_r2,how='inner',on=['node2'])
    edge_df['n1_n2_avg']=edge_df[['entropy_n1', 'entropy_n2']].mean(axis=1)
    edge_arr=edge_df.to_numpy()
    edge_df.to_csv("/localhome/pabitra/PD_network/edge_entropy.csv",index=None)
    
    ## iterating over edges
    
    ## log value handle
    def log_val(a,b):
        if a>0:
            try: return log2(a/b)
            except ZeroDivisionError: return 0
        else:
            return 0
        
    ## kl_divergence calculation    
    def kl_divergence(m1,m2):
        return sum(m1[i]*log_val(m1[i],m2[i]) for i in range(len(m1)))
    
    # calculate the jensen-shannon divergence
    def jensenshannon(n1,n2,W):
        ind1=n1
        ind2=n2
        m=0.5 * (W[ind1]+W[ind2])
        res= 0.5 * kl_divergence(W[ind1],m) + 0.5 * kl_divergence(W[ind2],m)
        return res
    
    
    with open("/localhome/pabitra/PD_network/PD_heteronet_link_entropy_text.txt",'w') as out:
        for k1 in range(len(edge_arr)):
            js_div=jensenshannon(int(edge_arr[k1][0]),int(edge_arr[k1][1]),W)
            le= 0.5 * (edge_arr[k1][4] + js_div)
            out.write("%d\t%d\t%s\n"%(int(edge_arr[k1][0]),int(edge_arr[k1][1]),le))
            
    weighted_df=pd.read_csv("/localhome/pabitra/PD_network/PD_heteronet_link_entropy_text.txt",sep='\t',header=None)
    weighted_df.columns=['entity1','entity2','link_weight']
    weighted_df.to_csv("/localhome/pabitra/PD_network/PD_heteronet_link_entropy.csv",index=None)
    d_entropy.close()
    
hf.close()
