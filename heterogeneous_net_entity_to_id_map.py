#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 23:35:10 2021

@author: saikat
"""

import pandas as pd


all_entity= pd.read_csv("/home/saikat/diabetes/final_T2DM_all_entity_file.csv")
all_entity=all_entity.drop(columns=['ID'])

biobert_concept_map= pd.read_csv("/home/saikat/biobert-pytorch/embedding/T2DM_entity_to_id_map.csv")

biobert_entity_map= pd.merge(biobert_concept_map,all_entity,how='inner',on=['entity_concept'])
biobert_entity_map=biobert_entity_map[['ID','entity','entity_concept','entity_type']]
entity_id_map=biobert_entity_map.drop(columns=['entity_concept'])

biobert_entity_map.to_csv("/home/saikat/diabetes/biobert_entity_id_map.csv",sep=',',index=None)
entity_id_map.to_csv("/home/saikat/diabetes/final_entity_id_map_T2DM.csv",sep=',',index=None)

## replace entity wih IDs in the corresponding edges

hetero_net= pd.read_csv("/home/saikat/diabetes/final_hetero_bidirectional_network_with_edge_types.csv")
hetero_net = hetero_net.dropna().reset_index(drop=True)
hetero_net = hetero_net.drop(columns=['entity1_type','entity2_type','combined_entity_type','entity_pair_type'])
# hetero_net=hetero_net[['entity1','entity2']]
entity_id_map=entity_id_map[['entity','ID']]
entity_id_map=entity_id_map.drop_duplicates()

entity_id_dict=dict(zip(entity_id_map.entity,entity_id_map.ID))

# hetero_net=hetero_net.applymap(entity_id_dict.get)
hetero_net['entity1']=hetero_net['entity1'].map(entity_id_dict)
hetero_net['entity2']=hetero_net['entity2'].map(entity_id_dict)
hetero_net=hetero_net.dropna()
# hetero_net_final=hetero_net[hetero_net.isna().any(axis=1)]
hetero_net.entity1=hetero_net.entity1.astype(int)
hetero_net.entity2=hetero_net.entity2.astype(int)


hetero_net.to_csv("/home/saikat/diabetes/final_entity_id_map_hetero_net.csv",index=None)




