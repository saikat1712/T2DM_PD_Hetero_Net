#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 19:55:56 2021

@author: saikat
"""
import numpy as np
import pandas as pd


weights=[]

### selecting max edge_betweennness column value entries

df_ptm_ptm=pd.read_csv("/home/saikat/Epigenomic_proj/ptm_ptm_edge_betweenness.csv")
col_val=df_ptm_ptm["Edge_betweennes_weight"]
max_val=col_val.max()
df_ptm_ptm_selected=df_ptm_ptm.loc[df_ptm_ptm["Edge_betweennes_weight"] >= max_val]
df_ptm_ptm_selected.to_csv("/home/saikat/Epigenomic_proj/ptm_ptm_with_max_edge_betweenness.txt",sep='\t',header=False,index=None)


### combining the selected ptm-ptm connection to the Amy_ptm network

amy_ptm=[]
with open("/home/saikat/Epigenomic_proj/amyloid_with_ptm_prots_associations.txt") as f:
    for line in f:
        ind=line.strip('\n').split('\t')
        amy_ptm.append((ind[0],ind[1]))
        
ptm_ptm=[]
with open("/home/saikat/Epigenomic_proj/ptm_ptm_with_max_edge_betweenness.txt") as f:
    for line in f:
        ind=line.strip('\n').split('\t')
        ptm_ptm.append((ind[0],ind[1]))
        
final_amy_ptm= amy_ptm+ptm_ptm

with open("/home/saikat/Epigenomic_proj/final_amyloid_ppi_ptm_network.txt",'w') as out:
    for k1,k2 in final_amy_ptm:
        out.write("%s\t%s\n"%(k1,k2))
    




    
    

        