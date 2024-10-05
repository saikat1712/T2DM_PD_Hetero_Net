#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 20:36:41 2021

@author: saikat
"""

import re
import pandas as pd

### combining the snps from epistasis interaction of T2DM
    
df_snp=pd.read_csv("/home/saikat/Desktop/plink.epi.cc.txt",sep='\s+')

s1=list(df_snp.SNP1)
s2=list(df_snp.SNP2)
        
all_snps=list(set(s1+s2))
df_all_snps=pd.DataFrame(all_snps,columns=['rsID'])


df_awesome_data=pd.read_csv("/home/saikat/Datasets/awesome-all.tsv",sep='\s+')

df_snp_ptm= pd.merge(df_all_snps, df_awesome_data, how="inner",on=['rsID'])
svalue=df_snp_ptm['O-GalNAc'] + df_snp_ptm['O-GlcNAc']
df_snp_ptm['OGly']=svalue

df_snp_ptm=df_snp_ptm.drop(columns=['O-GalNAc','O-GlcNAc'])

df_snp_ptm.to_csv("/home/saikat/Heterogeneous_diabetes/T2DM_snp_ptm.csv",sep=',',index=False)

df_snp_ptm_final=df_snp_ptm.drop(columns=['Symbol','ENSP','AA','Change','N-t-Ace','Exp','Score','Ref','Alt'])
# df_snp_ptm_final = df_snp_ptm_final.loc[~((df_snp_ptm_final['Phos'] == 0) & (df_snp_ptm_final['Ubi'] == 0)&(df_snp_ptm_final['Meth'] == 0)&(df_snp_ptm_final['SUMO'] == 0)&(df_snp_ptm_final['O-GalNAc'] == 0)&(df_snp_ptm_final['O-GlcNAc'] == 0)&(df_snp_ptm_final['N-Gly'] == 0)&(df_snp_ptm_final['K-Ace'] == 0))]
# df_snp_ptm_final.to_csv("/home/saikat/Heterogeneous_diabetes/T2DM_snp_ptm_temp.txt",sep='\t',index=False)

with open("/home/saikat/Heterogeneous_diabetes/T2DM_snp_ptm_final.txt",'w') as out:
    for (idx,row) in df_snp_ptm_final.iterrows():
        if row.loc['Phos']!=0.0:
            out.write("%s\t%s\t%s\n"%(row.loc['rsID'],'Phosphorylation',row.loc['Phos']))
        if row.loc['Ubi']!=0.0:
            out.write("%s\t%s\t%s\n"%(row.loc['rsID'],'Ubiquitination',row.loc['Ubi']))
        if row.loc['Meth']!=0.0:
            out.write("%s\t%s\t%s\n"%(row.loc['rsID'],'Methylation',row.loc['Meth']))
        if row.loc['SUMO']!=0.0:
            out.write("%s\t%s\t%s\n"%(row.loc['rsID'],'Sumoylation',row.loc['SUMO']))
        # elif row.loc['O-GalNAc']!=0:
        #     out.write("%s\t%s\t%s\n"%(row.loc['rsID'],'O-linked Glycosylation',row.loc['O-GalNAc']))
        if row.loc['OGly']!=0.0:
            out.write("%s\t%s\t%s\n"%(row.loc['rsID'],'O-linked Glycosylation',row.loc['OGly']))
        if row.loc['N-Gly']!=0.0:
            out.write("%s\t%s\t%s\n"%(row.loc['rsID'],'N-linked Glycosylation',row.loc['N-Gly']))
        

    