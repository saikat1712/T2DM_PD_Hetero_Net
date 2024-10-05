#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 17:39:44 2022

@author: saikat
"""
import pandas as pd


node_type_dict={}

node_types=['Pathway','Downregulated_gene','Upregulated_gene','Hypo_methylated_gene',
            'Hyper_methylated_gene','Downregulated_hyper_methylated_gene','Upregulated_hyper_methylated_gene',
            'Downregulated_hypo_methylated_gene','Upregulated_hypo_methylated_gene','Gene',
            'RSID_SNP','Amyloid_protein','PTM','ICD_T2DM']

i=0
for k in node_types:
    node_type_dict[k]=i
    i+=1

## Saving the node_type info in a pandas Dataframe
    
df_node_types=pd.DataFrame(list(node_type_dict.items()),columns=['entity_type','entity_type_id'])
df_node_types.to_csv("/home/saikat/Epigenomic_proj/node_type_dict.csv",index=None)

# m=df.to_dict(orient='dict')

