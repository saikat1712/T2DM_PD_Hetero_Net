#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 23:47:28 2022

@author: saikat
"""
import pandas as pd
import dgl
from dgl.data import DGLDataset
import torch
from ast import literal_eval 
import numpy as np


nodes_df = pd.read_csv("/home/saikat/OpenHGNN_test/My_Hetero_net_data_T2DM_dummy/T2DM_Hetero/final_node_data.csv")
edges_df = pd.read_csv("/home/saikat/OpenHGNN_test/My_Hetero_net_data_T2DM_dummy/T2DM_Hetero/final_edge_data.csv")        

nodes_df["feat"] = nodes_df["feat"].apply(lambda x: literal_eval(x))

# batched_outputs = torch.from_numpy(np.asarray(nodes_df["feat"].tolist()))



class T2DM_Hetero_Dataset(DGLDataset):
    def __init__(self):
        super().__init__(name='T2DM_Hetero')
        
    def process(self):
        nodes_data = nodes_df
        edges_data = edges_df
        node_features = torch.from_numpy(np.asarray(nodes_data["feat"].tolist()))
        node_labels = torch.from_numpy(nodes_data['label'].astype('category').cat.codes.to_numpy())
        edge_labels = torch.from_numpy(edges_data['label'].astype('category').cat.codes.to_numpy())
        edge_features = torch.from_numpy(edges_data['edge_weight'].to_numpy())
        edges_src = torch.from_numpy(edges_data['src_id'].to_numpy())
        edges_dst = torch.from_numpy(edges_data['dst_id'].to_numpy())
        self.graph = dgl.graph((edges_src,edges_dst),
                                num_nodes = nodes_data.shape[0])
        self.graph.ndata['feat'] = node_features
        self.graph.ndata['label'] = node_labels
        self.graph.edata['label'] = edge_labels
        self.graph.edata['weight'] = edge_features
    
    def __getitem__(self,i):
        return self.graph
    
    def __len__(self):
        return 1
    
dataset = T2DM_Hetero_Dataset()

graph = dataset[0]

print(graph)
        