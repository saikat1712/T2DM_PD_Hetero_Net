#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  2 15:19:04 2022

@author: saikat
"""

import pandas as pd

edges_df = pd.read_csv("/home/saikat/OpenHGNN_test/My_Hetero_net_data_T2DM_dummy/final_fully_weighted_hetero_net.csv")

edges_df.edge_type_id = edges_df.edge_type_id.astype(int)

for (edge_type), group in edges_df.groupby(['edge_type_id']):
    group.to_csv(f'T2DM_hetero_edges/edges_{edge_type}.csv', index=False)