#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 09:09:02 2021

@author: saikat
"""

## amyloid invivo and invitro central precursors to ICD- E11.8 code mappings
import re
import pandas as pd
Amy_invivo_vitro_central=[]
Amy_central_prot_gene_prot_map = []

with open("/home/saikat/Epigenomic_proj/uniprot_gene.txt") as f:
    for line in f:
        ind= line.strip('\n').split('\t')
        if ';' in ind[0]:
            y=re.findall('([^; \s+]+)',ind[0])
            Amy_invivo_vitro_central.append(y[0])
            Amy_invivo_vitro_central.append(y[1])
            Amy_central_prot_gene_prot_map.append((y[0],ind[1]))
            Amy_central_prot_gene_prot_map.append((y[1],ind[1]))
        else:
            Amy_invivo_vitro_central.append(ind[0])
            Amy_central_prot_gene_prot_map.append((ind[0],ind[1]))
            
central_gene_to_prot_df = pd.DataFrame(Amy_central_prot_gene_prot_map, columns = ['Gene', 'Central_protein'])

        
with open("/home/saikat/Epigenomic_proj/Amyloid_central_prot_to_ICD-10_E11.8.txt",'w') as out:
    for k in Amy_invivo_vitro_central:
        out.write("%s\t%s\n"%(k,'E11.8'))
        
central_gene_icd_df = pd.read_csv("/home/saikat/Epigenomic_proj/Amyloid_central_prot_to_ICD-10_E11.8.txt",
                                   sep='\t')

central_gene_icd_df.columns = ['Gene','ICD-10-T2DM']


final_central_prot_to_icd_pd = pd.merge(central_gene_icd_df, central_gene_to_prot_df,
                                       how='inner', on=['Gene'] )

final_central_prot_to_icd_pd = final_central_prot_to_icd_pd.drop(columns=['Gene'])

final_central_prot_to_icd_pd = final_central_prot_to_icd_pd[['Central_protein','ICD-10-T2DM']]

final_central_prot_to_icd_pd = final_central_prot_to_icd_pd.drop_duplicates()

final_central_prot_to_icd_pd.to_csv('/home/saikat/Epigenomic_proj/Amyloid_central_id_to_ICD-10_E11.8.csv',
                                    index=None, header=True)
        
        


