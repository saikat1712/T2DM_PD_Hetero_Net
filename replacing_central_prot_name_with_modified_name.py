#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 23:58:06 2022

@author: saikat
"""

import pandas as pd
import regex as re

### Amyloid_ppi_ptm network dataframe ###

final_df_amyloid_ppi_ptm_net=pd.read_csv("/home/saikat/Epigenomic_proj/final_amyppi_ptm_network_with_uniprot_id.csv")
final_df_amyloid_ppi_ptm_net=final_df_amyloid_ppi_ptm_net.rename(columns={'node1':'entity1','node2':'entity2'})

### Edge contracted pathway_icd_central_prot_snp network ##

icd_central_prot_name = pd.read_csv('/home/saikat/diabetes/icd_to_edge_contracted_names.csv')

icd_central_prot_map = dict(zip(icd_central_prot_name.n1, icd_central_prot_name.n2))

final_df_amyloid_ppi_ptm_net = final_df_amyloid_ppi_ptm_net.replace({'entity1': icd_central_prot_map,'entity2':icd_central_prot_map})

final_df_amyloid_ppi_ptm_net.to_csv('/home/saikat/diabetes/central_prot_replaced_newly_named_amy_ppi_net.csv', index=None)


