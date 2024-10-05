#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 20:36:14 2021

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

hetero_net= pd.read_csv("/home/saikat/diabetes/final_heterogeneous_network.csv")
hetero_net=hetero_net[['entity1','entity2']]
h_l=hetero_net['entity1'].tolist()+hetero_net['entity2'].tolist()
h_l=list(set(h_l))
hnet=pd.DataFrame(h_l,columns=['entity'])
hnet=hnet.drop_duplicates()

entity_id_map=entity_id_map[['entity','ID']]
entid=list(set(entity_id_map['entity'].tolist()))
entity_id_map=entity_id_map.drop_duplicates()
temp=list(set(h_l)-set(entid))
# entity_id_dict=dict(zip(entity_id_map.entity,entity_id_map.ID))

# # hetero_net=hetero_net.applymap(entity_id_dict.get)
# hetero_net=hetero_net[['entity1','entity2']]
# hetero_net["comb"]= hetero_net['entity1'].append(hetero_net['entity2']).reset_index(drop=True)
# hetero_net=hetero_net.drop(columns=['entity1','entity2'])

# hetero_net['id']=hetero_net['comb'].map(entity_id_dict)
# # hetero_net['entity2']=hetero_net['entity2'].map(entity_id_dict)
# hetero_net_final=hetero_net[hetero_net.isna().any(axis=1)]
# # hetero_net_final=hetero_net_final[['entity1','entity2']]
# # hetero_net_final.entity1=hetero_net_final.entity1.astype(int)
# # hetero_net_final.entity2=hetero_net_final.entity2.astype(int)



# hetero_net_final.to_csv("/home/saikat/diabetes/final_entity_id_map_hetero_net.csv",index=None)




