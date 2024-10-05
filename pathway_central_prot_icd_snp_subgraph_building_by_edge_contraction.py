#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 15:13:52 2022

@author: saikat
"""

import pandas as pd
from os import listdir
import networkx as nx

## pathway to icd-E11.8 network ##

path= "/home/saikat/diabetes/pathway_to_ICD_for_each_modules/"

path_icd_frames=[]
for filename in listdir("/home/saikat/diabetes/pathway_to_ICD_for_each_modules"):
    df_path_icd=pd.read_csv(path+filename)
    path_icd_frames.append(df_path_icd)

final_df_path_icd=pd.concat(path_icd_frames,ignore_index=True)
final_df_path_icd=final_df_path_icd.dropna()
final_df_path_icd=final_df_path_icd.rename(columns={'node':'entity1','ICD':'entity2'}) 


## SNP-RSID to icd-E11.8 ##

final_df_snp_icd= pd.read_csv("/home/saikat/Heterogeneous_diabetes/T2DM_RSIDs_to_ICD_only.csv")
final_df_snp_icd=final_df_snp_icd.rename(columns={'rsID':'entity1','ICD':'entity2'})

## Amyloid_central_protein to icd-E11.8 ##

final_df_amy_central_icd=pd.read_csv("/home/saikat/Epigenomic_proj/Amyloid_central_id_to_ICD-10_E11.8.csv")
final_df_amy_central_icd=final_df_amy_central_icd.rename(columns={'Central_protein':'entity1','ICD-10-T2DM':'entity2'})

## integration of all dataframes to build a single subgraph dataframe ##

subnet_frames = [final_df_path_icd, final_df_snp_icd, final_df_amy_central_icd]

hetero_subgraph_df = pd.concat(subnet_frames,ignore_index=True)

G=nx.from_pandas_edgelist(hetero_subgraph_df,'entity1','entity2') ## building subgraph from dataframe

## Edge contraction algorithm on the subgraph ##

mapping = {}
contract_edge = []

central_amy_icd = final_df_amy_central_icd.values.tolist()

for i in range(len(central_amy_icd)):
    contract_edge.append(tuple(central_amy_icd[i]))
    
for k in contract_edge:
    G_c = nx.contracted_edge(G,k,self_loops=True)
    mapping[k[0]] = k[0] + '_' + k[1] 
    G_c = nx.relabel_nodes(G_c,mapping)

df_G_c = nx.to_pandas_edgelist(G_c)

# nx.draw(G_c,with_labels = True)

df_G_c = df_G_c.rename(columns={'source':'entity1','target':'entity2'})

df_G_c.to_csv('/home/saikat/diabetes/pathway_icd_snp_central_amy_prot_subgraph_after_edge_contract.csv',index=None)
    
## making the central amyloid to modified names ##

mapped_df = pd.DataFrame(mapping.items(), columns=['n1', 'n2'])

mapped_df.to_csv('/home/saikat/diabetes/icd_to_edge_contracted_names.csv',index=None)

