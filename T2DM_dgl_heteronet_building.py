#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 01:11:13 2022

@author: saikat
"""

import pandas as pd
import locale
from locale import atof


df1=pd.read_csv("/home/saikat/OpenHGNN_test/My_Hetero_net_data_T2DM_dummy/T2DM_Hetero/final_T2DM_all_entity_file.csv")

df1.entity_type_id = df1.entity_type_id.astype(int)

df2 = pd.read_csv("/home/saikat/OpenHGNN_test/My_Hetero_net_data_T2DM_dummy/T2DM_Hetero/T2DM_entity_to_id_map.csv")

df_entity = pd.merge(df1,df2, how='inner', on=['ID','entity_concept'])

df_entity = df_entity.drop(columns=['entity_concept'])

### Taking biobert embeddings #####
df_biobert=pd.read_csv("/home/saikat/OpenHGNN_test/My_Hetero_net_data_T2DM_dummy/T2DM_Hetero/T2DM_entity_embedding.csv",header=None)
df_biobert['ID'] = df_biobert.index

## merging two dataframes df1_entity and df_biobert

df_final_node_data = pd.merge(df_entity, df_biobert, how='inner', on=['ID'])

df_final_node_data['feat'] = df_final_node_data[df_final_node_data.columns[4:]].apply(lambda x: ','.join(x.dropna().astype(str)), axis=1)


df_final_node_data = df_final_node_data.drop(df_final_node_data.columns[4:772], axis=1)
df_final_node_data = df_final_node_data.rename(columns={'ID':'node_id','entity_type_id':'label'})
df_final_node_data.to_csv("/home/saikat/OpenHGNN_test/My_Hetero_net_data_T2DM_dummy/T2DM_Hetero/final_node_data.csv",index=False)

############################### Edge Data ######################

edges_df = pd.read_csv("/home/saikat/OpenHGNN_test/My_Hetero_net_data_T2DM_dummy/T2DM_Hetero/final_fully_weighted_hetero_net.csv")

edges_df.edge_type_id = edges_df.edge_type_id.astype(int)

df_final_edge_data = edges_df

df_final_edge_data = df_final_edge_data.rename(columns={'entity1':'src_id','entity2':'dst_id','edge_type_id':'label'})

df_final_edge_data = df_final_edge_data.drop(columns=['entity_pair_type','bidirect'])

df_final_edge_data.to_csv("/home/saikat/OpenHGNN_test/My_Hetero_net_data_T2DM_dummy/T2DM_Hetero/final_edge_data.csv",index=None)

#################### DGL graph building ##################

# import dgl
# from dgl.data import DGLDataset
# import torch
# import os

# class T2DM_Hetero_Dataset(DGLDataset):
#     def __init__(self):
#         super().__init__(name='T2DM_Hetero')
        
#     def process(self):
#         nodes_data = df_final_node_data
#         edges_data = df_final_edge_data        
#         node_features = torch.from_numpy(nodes_data['feat'].to_numpy())
#         node_labels = torch.from_numpy(nodes_data['label'].astype('category').cat.codes.to_numpy())
#         edge_features = torch.from_numpy(edges_data['edge_weight'].to_numpy())
#         edges_src = torch.from_numpy(edges_data['src_id'].to_numpy())
#         edges_dst = torch.from_numpy(edges_data['dst_id'].to_numpy())
#         self.graph = dgl.graph((edges_src,edges_dst),
#                                num_nodes = nodes_data.shape[0])
#         self.graph.ndata['feat'] = node_features
#         self.graph.ndata['label'] = node_labels
#         self.graph.edata['weight'] = edge_features
    
#     def __getitem__(self,i):
#         return self.graph
    
#     def __len__(self):
#         return 1
    
# dataset = T2DM_Hetero_Dataset()

# graph = dataset[0]

# print(graph)
        
