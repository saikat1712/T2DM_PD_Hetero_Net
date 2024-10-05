#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 04:22:47 2021

@author: saikat
"""

import pandas as pd

df_hyper= pd.read_csv("/home/saikat/Heterogeneous_diabetes/diabetes_2_Methylation_overlap/Overlapping_T2DM_DM_genes_hypermethylated.csv")

#Get the indexes which are repetative with the split 
df_hyper['SigGenesInSet'] = df_hyper['SigGenesInSet'].str.split(',')
df_hyper = df_hyper.explode('SigGenesInSet')


df_hypo= pd.read_csv("/home/saikat/Heterogeneous_diabetes/diabetes_2_Methylation_overlap/Overlapping_T2DM_DM_genes_hypomethylated_with_DMR_regions.csv")
df_hypo['SigGenesInSet'] = df_hypo['SigGenesInSet'].str.split(',')
df_hypo = df_hypo.explode('SigGenesInSet')

    
## Differentially expressed genes 

df_DEGs= pd.read_csv("/home/saikat/Heterogeneous_diabetes/diabetes_2_Methylation_overlap/diffrential_genes_desired_cols.csv")

df_DEGs_only= df_DEGs[['SYMBOL']]

df_DEGs_only= df_DEGs_only.rename(columns={'SYMBOL':'SigGenesInSet'})

## intersection with hyper methylated enriched genes

DEGs_overlap_hyper= pd.merge(df_DEGs_only, df_hyper, how='inner',on=['SigGenesInSet'])
DEGs_overlap_hyper=DEGs_overlap_hyper.drop_duplicates()
DEGs_hyper = list(set(DEGs_overlap_hyper['SigGenesInSet'].tolist()))

with open("/home/saikat/Heterogeneous_diabetes/diabetes_2_Methylation_overlap/hypermethylated_DEGs.txt",'w') as out:
    for k1 in DEGs_hyper:
        out.write("%s\n"%k1)
        
DEGs_overlap_hyper= DEGs_overlap_hyper.rename(columns={'SigGenesInSet':'Hypermethylated_DEGs'})
DEGs_overlap_hyper= DEGs_overlap_hyper.drop(columns=['Unnamed: 0'])
DEGs_overlap_hyper.to_csv("/home/saikat/Heterogeneous_diabetes/diabetes_2_Methylation_overlap/Hypermethylated_DEGs_with_GO_enriched.csv",sep=',',index=False)

## intersection with hypo methylated enriched genes

DEGs_overlap_hypo= pd.merge(df_DEGs_only, df_hypo, how='inner',on=['SigGenesInSet'])
DEGs_overlap_hypo= DEGs_overlap_hypo.drop_duplicates()
DEGs_hypo = list(set(DEGs_overlap_hypo['SigGenesInSet'].tolist()))
with open("/home/saikat/Heterogeneous_diabetes/diabetes_2_Methylation_overlap/hypomethylated_DEGs.txt",'w') as out:
    for k2 in DEGs_hypo:
        out.write("%s\n"%k2)
        
DEGs_overlap_hypo= DEGs_overlap_hypo.rename(columns={'SigGenesInSet':'Hypomethylated_DEGs'})
DEGs_overlap_hypo= DEGs_overlap_hypo.drop(columns=['Unnamed: 0'])
DEGs_overlap_hypo.to_csv("/home/saikat/Heterogeneous_diabetes/diabetes_2_Methylation_overlap/Hypomethylated_DEGs_with_GO_enriched.csv",sep=',',index=False)



