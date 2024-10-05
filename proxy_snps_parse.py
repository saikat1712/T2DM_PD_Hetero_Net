#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 17:51:39 2021

@author: saikat
"""

import pandas as pd

snipa_list=[]
seen=set()

with open("/home/saikat/diabetes/diabetes2_SNP_Proxy/final_diabetes2_proxys.txt") as f:
    for line in f:
        ind=line.strip('\n').split('\t')
        if (ind[1],ind[5]) not in seen:
            seen.add((ind[1],ind[5]))
            snipa_list.append((ind[1],ind[5]))
        else:
            pass
        
        
df1=pd.DataFrame(snipa_list,index=None)
n1_header=df1.iloc[0]        
df1=df1[1:]
df1.columns=n1_header

# vep_diabetes=[]
# vep_diabetes.append(('chr','RSID','BP','ref','alt','pheno'))
# with open("/home/saikat/Heterogeneous_diabetes/diabetes_var_parse_final.txt") as f:
#     for line in f:
#         ind=line.strip('\n').split('\t')
#         vep_diabetes.append((ind[0],ind[1],ind[2],ind[3],ind[4],ind[5]))
        
# df2=pd.DataFrame(vep_diabetes,index=None)
# n2_header=df2.iloc[0]        
# df2=df2[1:]
# df2.columns=n2_header

# final_df=pd.merge(df1, df2, how='inner',on=['RSID'])

df2_gtex=pd.read_csv("/home/saikat/Heterogeneous_diabetes/gtx_Eur_liver_rsids_only.csv")

df2_gtex=df2_gtex.drop(columns="MAF",axis=1)

df_euro_liver=pd.merge(df1, df2_gtex, how="inner",on=['RSID'])

df_euro_liver.to_csv("/home/saikat/Heterogeneous_diabetes/final_diabetes_snps_euro_liver.csv",sep=',',header=True,index=False)


        

            