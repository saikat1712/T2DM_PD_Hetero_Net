#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 18:00:24 2022

@author: saikat
"""



## Creating the Node dataset with their corresponding Biobert trained 768 dimensional node embeddings

import pandas as pd
import numpy as np


df1=pd.read_csv("/home/saikat/OpenHGNN_test/My_Hetero_net_data_T2DM_dummy/final_T2DM_all_entity_file.csv")

df1.entity_type_id = df1.entity_type_id.astype(int)

df2 = pd.read_csv("/home/saikat/OpenHGNN_test/My_Hetero_net_data_T2DM_dummy/T2DM_entity_to_id_map.csv")

df_entity = pd.merge(df1,df2, how='inner', on=['ID','entity_concept'])

df_entity = df_entity.drop(columns=['entity_concept'])

### Taking biobert embeddings #####
df_biobert=pd.read_csv("/home/saikat/OpenHGNN_test/My_Hetero_net_data_T2DM_dummy/T2DM_entity_embedding.csv",header=None)
df_biobert['ID'] = df_biobert.index


## merging two dataframes df1_entity and df_biobert


df_final_node_embed = pd.merge(df_entity, df_biobert, how='inner', on=['ID'])

df_final_node_embed['feat'] = df_final_node_embed[df_final_node_embed.columns[4:]].apply(lambda x: ','.join(x.dropna().astype(str)), axis=1)


df_final_node_embed = df_final_node_embed.drop(df_final_node_embed.columns[4:772], axis=1)

df_final_node_embed.to_csv("/home/saikat/OpenHGNN_test/My_Hetero_net_data_T2DM_dummy/new_final_node_df.csv",index=False)

for (label), group in df_final_node_embed.groupby(['entity_type_id']):
      group.to_csv(f'T2DM_hetero_nodes/nodes_{label}.csv', index=False)


# final_node_arr = final_node_df.to_numpy()

# N=768 # Dimension of Biobert embedding
# np.savetxt('/home/saikat/Link_pred_jupyter_proj_2nd_work/My_Hetero_net_data_T2DM_dummy/node_data.dat',
#            final_node_arr, fmt='\t'.join(['%i'] + ['%s'] + ['%i']) +'\t' +','.join(['%1.15e']*N))
