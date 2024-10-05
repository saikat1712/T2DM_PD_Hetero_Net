#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 18:38:40 2022

@author: saikat
"""

import pandas as pd

## Making dictionary of node_types

node_type_dict={}

node_types=['Pathway','Downregulated_gene','Upregulated_gene','Hypo_methylated_gene',
            'Hyper_methylated_gene','Downregulated_hyper_methylated_gene','Upregulated_hyper_methylated_gene',
            'Downregulated_hypo_methylated_gene','Upregulated_hypo_methylated_gene','Gene',
            'RSID_SNP','Amyloid_protein','PTM','ICD_T2DM']

i=0
for k in node_types:
    node_type_dict[k]=i
    i+=1
    
df_node_types=pd.DataFrame(list(node_type_dict.items()),columns=['entity_type','entity_type_id'])
df_node_types.to_csv("/home/saikat/Epigenomic_proj/node_type_dict.csv",index=None)
    
#### edge dictionary ######

edge_type_dict={}

edge_types=[('pathway','interacts','pathway'),('gene','interacts','gene'),('pathway','interacts','gene'),
            ('snp','interacts','snp'),('snp','interacts','dmg'),('snp','interacts','ptm'),
            ('ptm','interacts','ptm'),('amyloid_protein','interacts','amyloid_protein'),('ptm','interacts','amyloid_protein'),
            ('pathway','interacts','icd'),('amyloid_central_protein','interacts','icd'),
            ('snp','interacts','icd')]

i=0
for k in edge_types:
    edge_type_dict[k]=i
    i+=1
    
df_edge_types=pd.DataFrame(list(edge_type_dict.items()),columns=['edge_type','edge_type_id'])
df_edge_types.to_csv("/home/saikat/Epigenomic_proj/edge_type_dict.csv",index=None)