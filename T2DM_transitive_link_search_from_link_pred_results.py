#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 20:29:06 2022

@author: saikat
"""

import pandas as pd

### Original bidirectional network for T2DM ####

df_t2dm = pd.read_csv("/home/saikat/diabetes/final_heterogeneous_network_bidirectional.csv")

df_t2dm = df_t2dm.drop(columns=['edge_weight'])

df_t2dm = df_t2dm[['entity1','entity2']]


## Pathway-Central_amyloid_icd 

df_path_CenDM = pd.read_csv('/home/saikat/diabetes/Diabetes_HAN_results/HAN_link_results/pathway_CenDM/neg_edges_test.csv')

df_path_CenDM = df_path_CenDM.drop(columns=['probability_score'])

df_path_CenDM = df_path_CenDM.rename(columns={'node1':'entity1','node2':'entity2'})

df_path_CenDM_merge = pd.merge(df_path_CenDM, df_t2dm, how = 'inner', on = ['entity1','entity2'])

## Only Unique Pathway_CenDM links, which are not present in the original graph

df_path_CenDM_unique = pd.merge(df_path_CenDM, df_path_CenDM_merge, on=['entity1','entity2'], how='outer', indicator=True).query("_merge != 'both'").drop('_merge', axis=1).reset_index(drop=True)

## Central_amyloid_icd_Amyloid-protein

df_CenDM_Amy = pd.read_csv('/home/saikat/diabetes/Diabetes_HAN_results/HAN_link_results/CenDM_Amy/neg_edges_test.csv')

df_CenDM_Amy = df_CenDM_Amy.drop(columns=['probability_score'])

df_CenDM_Amy = df_CenDM_Amy.rename(columns={'node1':'entity1','node2':'entity2'})

df_CenDM_Amy_merge = pd.merge(df_CenDM_Amy, df_t2dm, how = 'inner', on = ['entity1','entity2'])

## Only Unique CenDM_Amyloid-protein links, which are not present in the original graph

df_CenDM_Amy_unique = pd.merge(df_CenDM_Amy, df_CenDM_Amy_merge, on=['entity1','entity2'], how='outer', indicator=True).query("_merge != 'both'").drop('_merge', axis=1).reset_index(drop=True)

## Amyloid_ptm

df_Amy_ptm = pd.read_csv('/home/saikat/diabetes/Diabetes_HAN_results/HAN_link_results/Amy_PTM/neg_edges_test.csv')

df_Amy_ptm = df_Amy_ptm.drop(columns=['probability_score'])

df_Amy_ptm = df_Amy_ptm.rename(columns={'node1':'entity1','node2':'entity2'})

df_Amy_ptm_merge = pd.merge(df_Amy_ptm, df_t2dm, how = 'inner', on = ['entity1','entity2'])

## Only Unique Amyloid-protein_ptm links, which are not present in the original graph

df_Amy_ptm_unique = pd.merge(df_Amy_ptm, df_Amy_ptm_merge, on=['entity1','entity2'], how='outer', indicator=True).query("_merge != 'both'").drop('_merge', axis=1).reset_index(drop=True)

## Intersection between Pathway and Amyloid_protein

df_path_CenDM_unique_new = df_path_CenDM[['entity2','entity1']]

df_path_CenDM_unique_new = df_path_CenDM_unique_new.rename(columns={'entity2':'entity1',
                                                                    'entity1':'entity2'})

## Predicting links between Pathway and Amyloid_proteins

df_path_amy_predict = pd.merge(df_path_CenDM_unique_new, df_CenDM_Amy_unique, how='inner', on=['entity1'])

df_path_amy_predict = df_path_amy_predict.drop(columns=['entity1'])

df_path_amy_predict = df_path_amy_predict.rename(columns={'entity2_x':'entity2','entity2_y':'entity1'})

df_path_amy_predict = df_path_amy_predict[['entity1','entity2']]

df_path_amy_predict = df_path_amy_predict.drop_duplicates()

df_path_amy_predict.to_csv('/home/saikat/diabetes/Diabetes_HAN_results/predicted_pathway_amyloid_links.csv', index=False)


## Predicting links between Pathway and PTM 

df_Amy_ptm_unique = df_Amy_ptm_unique[['entity2','entity1']]

df_Amy_ptm_unique = df_Amy_ptm_unique.rename(columns={'entity2':'entity1','entity1':'entity2'})

df_Pathway_PTM_predicted_links = pd.merge(df_path_amy_predict, df_Amy_ptm_unique, how='inner', on=['entity1'])

df_Pathway_PTM_predicted_links = df_Pathway_PTM_predicted_links.drop(columns=['entity1'])

df_Pathway_PTM_predicted_links = df_Pathway_PTM_predicted_links.rename(columns={'entity2_x':'entity1','entity2_y':'entity2'})

df_Pathway_PTM_predicted_links = df_Pathway_PTM_predicted_links.drop_duplicates()

df_Pathway_PTM_predicted_links.to_csv('/home/saikat/diabetes/Diabetes_HAN_results/predicted_pathway_ptm_links.csv', index=False) 

## Pathway_Hypo-Methylation

df_path_hypo = pd.read_csv('/home/saikat/diabetes/Diabetes_HAN_results/HAN_link_results/Pathway_Hypo/neg_edges_test.csv')

df_path_hypo = df_path_hypo.drop(columns=['probability_score'])

df_path_hypo = df_path_hypo.rename(columns={'node1':'entity1','node2':'entity2'})

## Predicting links between hypomethylation and ptm via pathways

df_hypo_ptm_via_pathway = pd.merge(df_Pathway_PTM_predicted_links, 
                                   df_path_hypo, how='inner', on=['entity1'])

df_hypo_ptm_via_pathway.to_csv('/home/saikat/diabetes/Diabetes_HAN_results/T2DM_predicted_hypo_methyl_ptm_links.csv', index=False)


## snp link to amyloid_proteins

df_snp = pd.read_csv('/home/saikat/diabetes/Diabetes_HAN_results/HAN_link_results/snp_CenDM/neg_edges_test.csv')
df_snp = df_snp.drop(columns=['probability_score'])
df_snp = df_snp.rename(columns={'node1':'entity1', 'node2':'entity2'})
# df_snp = df_snp[['entity1','entity2']]
df_snp_merge = pd.merge(df_snp, df_t2dm, how = 'inner', on = ['entity1','entity2'])
df_snp_unique = pd.merge(df_snp, df_snp_merge, on=['entity1','entity2'], how='outer', indicator=True).query("_merge != 'both'").drop('_merge', axis=1).reset_index(drop=True)

df_snp_unique = df_snp_unique[['entity2','entity1']]

df_snp_unique = df_snp_unique.rename(columns={'entity2':'entity1','entity1':'entity2'})

df_snp_amyloid_predicted_links = pd.merge(df_snp_unique, df_CenDM_Amy_unique, how='inner', on=['entity1'])

df_snp_amyloid_predicted_links.to_csv('/home/saikat/diabetes/Diabetes_HAN_results/T2DM_snp_amyloid_links.csv',index=False)




