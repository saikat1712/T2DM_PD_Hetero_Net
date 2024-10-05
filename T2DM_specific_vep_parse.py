#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 20:58:30 2021

@author: saikat
"""

###### Mapping SNP RSIDs to the T2DM Phenotypes

import pandas as pd

T2DM_vep=[]
T2DM_RSID=[]

with open("/home/saikat/Desktop/diabetes2_variants_out_final.txt") as f:
    for line in f:
        if line.startswith('#') == False:
            ind=line.strip('\n').split('\t')
            if 'Diabetes Mellitus' in ind[7]:
                T2DM_vep.append((ind[0],ind[7]))
                T2DM_RSID.append(ind[0])
            else:
                pass
        else:
            pass
        
with open("/home/saikat/Heterogeneous_diabetes/diabetes2_vep_only_T2DM_DisgeNET.txt",'w') as out:
    for k1,k2 in T2DM_vep:
        out.write("%s\t%s\n"%(k1,k2))
        
T2DM_RSID=list(set(T2DM_RSID))

df_T2DM_vep=pd.DataFrame(T2DM_RSID)
df_T2DM_vep.columns=["rsID"]

### combining the snps from epistasis interaction of T2DM
    
df_snp=pd.read_csv("/home/saikat/Desktop/plink.epi.cc.txt",sep='\s+')

s1=list(df_snp.SNP1)
s2=list(df_snp.SNP2)
        
all_snps=list(set(s1+s2))
df_all_snps=pd.DataFrame(all_snps,columns=['rsID'])

df_snps_to_T2DM=pd.merge(df_T2DM_vep,df_all_snps,how="inner",on=['rsID'])
df_snps_to_T2DM['ICD']='E11.8'

df_snps_to_T2DM.to_csv("/home/saikat/Heterogeneous_diabetes/T2DM_RSIDs_to_ICD_only.csv",index=None,header=True)
