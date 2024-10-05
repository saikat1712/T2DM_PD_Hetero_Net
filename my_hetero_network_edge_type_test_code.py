#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 13:30:03 2022

@author: saikat
"""


import pandas as pd

## entity-entity_type dictionary ##


entities_df = pd.read_csv("/home/saikat/diabetes/final_T2DM_all_entity_file.csv")

entities_df = entities_df.drop(columns=['ID','entity_concept','entity_type_id'])

entities_df.set_index('entity', inplace=True)

entity_type_dict = entities_df.to_dict()['entity_type']

#### edge dictionary ######

edge_type_dict={}

edge_types= [['pathway','interacts','pathway'],['gene','interacts','gene'],['gene','interacts','downregulated_gene'],
            ['downregulated_gene','rev_interacts','gene'],['gene','interacts','upregulated_gene'],['upregulated_gene','rev_interacts','gene'],
            ['gene','interacts','hypo_methylated_gene'],['hypo_methylated_gene','rev_interacts','gene'],['gene','interacts','hyper_methylated_gene'],['hyper_methylated_gene','rev_interacts','gene'],
            ['gene','interacts','upregulated_hypo_methylated_gene'],['upregulated_hypo_methylated_gene','rev_interacts','gene'],
            ['gene','interacts','downregulated_hypo_methylated_gene'],['downregulated_hypo_methylated_gene','rev_interacts','gene'],
            ['gene','interacts','upregulated_hyper_methylated_gene'],['upregulated_hyper_methylated_gene','rev_interacts','gene'],
            ['gene','interacts','downregulated_hyper_methylated_gene'],['downregulated_hyper_methylated_gene','rev_interacts','gene'],
            ['pathway','interacts','gene'],['gene','rev_interacts','pathway'],
            ['pathway','interacts','downregulated_gene'],['downregulated_gene','rev_interacts','pathway'],['pathway','interacts','upregulated_gene'],
            ['upregulated_gene','rev_interacts','pathway'],['pathway','interacts','hypo_methylated_gene'],['hypo_methylated_gene','rev_interacts','pathway'],
            ['pathway','interacts','hyper_methylated_gene'],['hyper_methylated_gene','rev_interacts','pathway'],
            ['pathway','interacts','downregulated_hypo_methylated_gene'],['downregulated_hypo_methylated_gene','rev_interacts','pathway'],['pathway','interacts','upregulated_hypo_methylated_gene'],
            ['upregulated_hypo_methylated_gene','rev_interacts','pathway'],['pathway','interacts','downregulated_hyper_methylated_gene'],['downregulated_hyper_methylated_gene','rev_interacts','pathway'],['pathway','interacts','upregulated_hyper_methylated_gene'],['upregulated_hyper_methylated_gene','rev_interacts','pathway'],['downregulated_gene','interacts','downregulated_gene'],
            ['upregulated_gene','interacts','upregulated_gene'],['rsid_snp','interacts','rsid_snp'],['rsid_snp','interacts','hypo_methylated_gene'],['hypo_methylated_gene','rev_interacts','rsid_snp'],
            ['rsid_snp','interacts','hyper_methylated_gene'],['hyper_methylated_gene','rev_interacts','rsid_snp'],['rsid_snp','interacts','downregulated_hypo_methylated_gene'],['downregulated_hypo_methylated_gene','rev_interacts','rsid_snp'],
            ['rsid_snp','interacts','upregulated_hypo_methylated_gene'],['upregulated_hypo_methylated_gene','rev_interacts','rsid_snp'],['rsid_snp','interacts','downregulated_hyper_methylated_gene'],['downregulated_hyper_methylated_gene','rev_interacts','rsid_snp'],['rsid_snp','interacts','upregulated_hyper_methylated_gene'],
            ['upregulated_hyper_methylated_gene','rev_interacts','rsid_snp'],['rsid_snp','interacts','ptm'],['ptm','rev_interacts','rsid_snp'],['amyloid_protein','interacts','amyloid_protein'],
            ['ptm','interacts','ptm'],['ptm','interacts','amyloid_protein'],['amyloid_protein','rev_interacts','ptm'],['pathway','interacts','icd_t2dm'],['icd_t2dm','rev_interacts','pathway'],
            ['central_amyloid_protein','interacts','icd_t2dm'],['icd_t2dm','rev_interacts','central_amyloid_protein'],['rsid_snp','interacts','icd_t2dm'],['icd_t2dm','rev_interacts','rsid_snp']]


i=0
for k in edge_types:
    edge_type_dict[tuple(k)]=i
    i+=1
    
edge_pair_types= [['pathway','pathway'],['gene','gene'],['gene','downregulated_gene'],
            ['downregulated_gene','gene'],['gene','upregulated_gene'],['upregulated_gene','gene'],
            ['gene','hypo_methylated_gene'],['hypo_methylated_gene','gene'],['gene','hyper_methylated_gene'],['hyper_methylated_gene','gene'],
            ['gene','upregulated_hypo_methylated_gene'],['upregulated_hypo_methylated_gene','gene'],
            ['gene','downregulated_hypo_methylated_gene'],['downregulated_hypo_methylated_gene','gene'],
            ['gene','upregulated_hyper_methylated_gene'],['upregulated_hyper_methylated_gene','gene'],
            ['gene','downregulated_hyper_methylated_gene'],['downregulated_hyper_methylated_gene','gene'],
            ['pathway','gene'],['gene','pathway'],
            ['pathway','downregulated_gene'],['downregulated_gene','pathway'],['pathway','upregulated_gene'],
            ['upregulated_gene','pathway'],['pathway','hypo_methylated_gene'],['hypo_methylated_gene','pathway'],['pathway','hyper_methylated_gene'],['hyper_methylated_gene','pathway'],
            ['pathway','downregulated_hypo_methylated_gene'],['downregulated_hypo_methylated_gene','pathway'],['pathway','upregulated_hypo_methylated_gene'],
            ['upregulated_hypo_methylated_gene','pathway'],['pathway','downregulated_hyper_methylated_gene'],['downregulated_hyper_methylated_gene','pathway'],['pathway','upregulated_hyper_methylated_gene'],['upregulated_hyper_methylated_gene','pathway'],['downregulated_gene','downregulated_gene'],
            ['upregulated_gene','upregulated_gene'],['rsid_snp','rsid_snp'],['rsid_snp','hypo_methylated_gene'],['hypo_methylated_gene','rsid_snp'],
            ['rsid_snp','hyper_methylated_gene'],['hyper_methylated_gene','rsid_snp'],['rsid_snp','downregulated_hypo_methylated_gene'],['downregulated_hypo_methylated_gene','rsid_snp'],
            ['rsid_snp','upregulated_hypo_methylated_gene'],['upregulated_hypo_methylated_gene','rsid_snp'],['rsid_snp','downregulated_hyper_methylated_gene'],['downregulated_hyper_methylated_gene','rsid_snp'],['rsid_snp','upregulated_hyper_methylated_gene'],
            ['upregulated_hyper_methylated_gene','rsid_snp'],['rsid_snp','ptm'],['ptm','rsid_snp'],['amyloid_protein','amyloid_protein'],
            ['ptm','ptm'],['ptm','amyloid_protein'],['amyloid_protein','ptm'],['pathway','icd_t2dm'],['icd_t2dm','pathway'],
            ['central_amyloid_protein','icd_t2dm'],['icd_t2dm','central_amyloid_protein'],['rsid_snp','icd_t2dm'],['icd_t2dm','rsid_snp']]

edge_dict = {}


for i in range(len(edge_types)):
    edge_dict[tuple(edge_pair_types[i])] = edge_types[i]


Heterogeneous_Network_final = pd.read_csv("/home/saikat/diabetes/final_heterogeneous_network_bidirectional.csv")

# Heterogeneous_Network_final = Heterogeneous_Network_final.sample(frac=0.5, replace=True).reset_index(drop=True)                                                         

# Heterogeneous_Network_final = Heterogeneous_Network_final[:100]

Heterogeneous_Network_final = Heterogeneous_Network_final.drop(columns=['Edge_type'])

## Make a dictionary from entity id to entity types

Heterogeneous_Network_final = Heterogeneous_Network_final.assign(entity1_type = '',
                                                                entity2_type = '' )

# Heterogeneous_Network_final = Heterogeneous_Network_final[['entity1','entity2','Edge_weight','entity1_type','entity2_type']]

for index, row in Heterogeneous_Network_final.iterrows():
    a = row['entity1']
    b = row['entity2']
    for k,v in entity_type_dict.items():
        if a == k:            
            Heterogeneous_Network_final.at[index, 'entity1_type'] = entity_type_dict[a]
            # print(a,'\t',entity_type_dict[a])
        elif b == k:
            Heterogeneous_Network_final.at[index, 'entity2_type'] = entity_type_dict[b] 
            # print(b,'\t',entity_type_dict[b])
        else:
            pass 

    

## Making the combined entity_type in the Heterogeneous Network ###

# Heterogeneous_Network_final['combined_entity_type'] = Heterogeneous_Network_final[['entity1_type','entity2_type']].agg(','.join, axis=1)

Heterogeneous_Network_final['combined_entity_type'] = Heterogeneous_Network_final[['entity1_type','entity2_type']].values.tolist()

for index, row in Heterogeneous_Network_final.iterrows():
    for key, value in edge_dict.items():
        if row['combined_entity_type'] == list(key):
            Heterogeneous_Network_final.at[index, 'entity_pair_type'] = str(key)
            Heterogeneous_Network_final.at[index, 'edge_type_id'] = edge_type_dict[tuple(value)]
        else:
            pass
    
        

Heterogeneous_Network_final.to_csv("/home/saikat/diabetes/Heterogeneous_network_test.csv",index=None)        

        
