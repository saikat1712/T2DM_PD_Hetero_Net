#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 20:56:50 2021

@author: saikat

"""
from __future__ import print_function
import pandas as pd
import os



rsid_genes=[]

with open("/home/saikat/Heterogeneous_diabetes/gtx_Eur_liver_rsids_only.txt") as f:
    for line in f: 
        if line.startswith('chr')==False:
            ind=line.strip('\n').split('\t')
            rsid_genes.append((ind[1],ind[5]))
        else:
            pass
        
df_rsid_vep= pd.DataFrame(rsid_genes)
df_rsid_vep.columns=['RSID','gene_id']

### combining the snps from epistasis interaction of T2DM
    
df_snp=pd.read_csv("/home/saikat/Desktop/plink.epi.cc.txt",sep='\s+')

s1=list(df_snp.SNP1)
s2=list(df_snp.SNP2)
        
all_snps=list(set(s1+s2))
df_all_snps=pd.DataFrame(all_snps,columns=['RSID'])

## intersecting with only those RSIDs which are in the epistatsis interactions

df_rsid_vep=pd.merge(df_all_snps,df_rsid_vep,how='inner',on=['RSID'])


## RSID to hyper methylated genes (if exists)

try:
    df_hyper= pd.read_csv("/home/saikat/Heterogeneous_diabetes/diabetes_2_Methylation_overlap/Hyper_DEGs_ensembl_map.csv")
    df_hyper_vep_overlap=pd.merge(df_rsid_vep, df_hyper, how='inner',on=['gene_id'])
    df_hyper_vep_overlap=df_hyper_vep_overlap.drop(columns=['Unnamed: 0'])
    df_hyper_vep_overlap=df_hyper_vep_overlap.drop_duplicates()
    df_hyper_vep_overlap.to_csv("/home/saikat/Heterogeneous_diabetes/diabetes_2_Methylation_overlap/hyper_vep_overlap.csv",index=None,header=True)   # generate 'file not found error'
except EnvironmentError as e:      # OSError or IOError...
    print(os.strerror(e.errno)) 

        
        
# RSID to hypo methylated genes (if exists)

try:
    df_hypo= pd.read_csv("/home/saikat/Heterogeneous_diabetes/diabetes_2_Methylation_overlap/Hypo_DEGs_ensembl_map.csv")
    df_hypo_vep_overlap=pd.merge(df_rsid_vep, df_hypo, how='inner',on=['gene_id'])
    df_hypo_vep_overlap=df_hypo_vep_overlap.drop(columns=['Unnamed: 0'])
    df_hypo_vep_overlap=df_hypo_vep_overlap.drop_duplicates()
    df_hypo_vep_overlap.to_csv("/home/saikat/Heterogeneous_diabetes/diabetes_2_Methylation_overlap/hypo_vep_overlap.csv",index=None,header=True)
except EnvironmentError as e:      # OSError or IOError...
    print(os.strerror(e.errno)) 
