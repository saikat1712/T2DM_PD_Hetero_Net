#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 23:30:04 2021

@author: saikat
"""

import pandas as pd
import numpy as np

hetero_basic= pd.read_csv("/home/saikat/diabetes/final_entity_id_map_hetero_net.csv")

df1=hetero_basic[['entity1','entity2']]

## grouping on the basis of maximum edge_weight and discarding others ####

df_hetero_max_weight = hetero_basic.loc[hetero_basic.groupby(['entity1','entity2'])['edge_weight'].idxmax()]
df_hetero_max_weight = df_hetero_max_weight.reset_index()
df_hetero_max_weight = df_hetero_max_weight.drop(columns=['index'])

############# making hetero_link_entropy for all undirected edges #######
hetero_link_entropy1= pd.read_csv("/home/saikat/diabetes/heteronet_link_entropy.csv")
hetero_link_entropy2=hetero_link_entropy1[['entity2','entity1','link_weight']]
hetero_link_entropy2=hetero_link_entropy2.rename(columns={'entity2':'entity1','entity1':'entity2'})
link_frames=[hetero_link_entropy1,hetero_link_entropy2]
hetero_link_entropy=pd.concat(link_frames,ignore_index=True)

########################## merging actual hetero_net with link_entropy hetero_net ###############

final_hetero_net= pd.merge(df_hetero_max_weight,hetero_link_entropy, how='inner', on=['entity1','entity2'])
final_hetero_net=final_hetero_net.drop_duplicates()
final_weighted_hetero_net = final_hetero_net
final_weighted_hetero_net['edge_weight']= np.where(final_weighted_hetero_net['edge_weight'] == -9999, final_weighted_hetero_net['link_weight'], final_weighted_hetero_net['edge_weight'])
final_weighted_hetero_net=final_weighted_hetero_net.drop(columns=['link_weight'])

df = final_weighted_hetero_net

df['bidirect'] = (df.entity1+df.entity2).isin(df.entity2+df.entity1)

df.to_csv("/home/saikat/diabetes/final_fully_weighted_hetero_net.csv",index=None)

# hetero_diff=df_hetero_max_weight[~df_hetero_max_weight.index.isin(final_hetero_net.index)]

print("Program completed")