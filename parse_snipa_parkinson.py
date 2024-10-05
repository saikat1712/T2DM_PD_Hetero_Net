# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 06:34:28 2021

@author: ASUS
"""

import pandas as pd





df=pd.read_csv("D:\parkinson\parkinson_SNP_Proxy\parkinson_proxy_snps.csv", sep='\t')

cols_l= ['QRSID','RSID','R2']

df_proxy= df[cols_l]

df_proxy.to_csv(r"D:\parkinson\parkinson_SNP_Proxy\final_parkinson_proxys.txt",index=None, sep='\t',mode='a')

all_snp=[]

t1=[]
t2=[]

with open(r"D:\parkinson\parkinson_SNP_Proxy\final_parkinson_proxys.txt") as f:
    for line in f:
        if line.startswith('QRSID')==False:
            ind=line.strip('\n').split('\t')
            t1.append(ind[0])
            t2.append(ind[1])
        else:
            pass
        
all_snp=list(set(t1+t2))

with open(r"D:\parkinson\parkinson_SNP_Proxy\single_col_all_parkinson_snps.txt",'w') as out:
    for x in all_snp:
        out.write("%s\n"%x)

