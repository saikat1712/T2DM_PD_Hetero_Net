# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 09:25:29 2021

@author: ASUS
"""

import pandas as pd





df=pd.read_csv("/home/saikat/diabetes/diabetes2_SNP_Proxy/diabetes2_proxy_snps.csv", sep='\t')

cols_l= ['QRSID','RSID','R2','MAJOR','MINOR','MAF']


df_proxy= df[cols_l]

df_proxy.to_csv("/home/saikat/diabetes/diabetes2_SNP_Proxy/final_diabetes2_proxys.txt",index=None, sep='\t',mode='a')


all_snp=[]

t1=[]
t2=[]

with open("/home/saikat/diabetes/diabetes2_SNP_Proxy/final_diabetes2_proxys.txt") as f:
    for line in f:
        if line.startswith('QRSID')==False:
            ind=line.strip('\n').split('\t')
            t1.append(ind[0])
            t2.append(ind[1])
        else:
            pass
        
all_snp=list(set(t1+t2))

with open("/home/saikat/diabetes/diabetes2_SNP_Proxy/single_col_all_diabetes2_snps.txt",'w') as out:
    for x in all_snp:
        out.write("%s\n"%x)

        





