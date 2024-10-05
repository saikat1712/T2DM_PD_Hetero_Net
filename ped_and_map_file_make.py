#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 12:21:03 2021

@author: saikat
"""

import pandas as pd
import numpy as np


query_rsid=[]

with open("/home/saikat/diabetes/diabetes2_SNP_Proxy/final_diabetes2_proxys.txt") as f:
    for line in f:
        ind=line.strip('\n').split('\t')
        if ind[0]!=ind[1]:
            query_rsid.append(ind[0])
        else:
            pass
        
df1=pd.read_csv("/home/saikat/Heterogeneous_diabetes/query_proxy_info.csv",sep='\t')
df1.columns=['Query_RSID','Proxy_RSID','Query_ref','Query_alt','Proxy_ref','Proxy_alt','Query_pheno','Proxy_pheno']
df2=df1
df2=df2.assign(Final_pheno = lambda x: 0)

df2['Final_pheno']=np.where(df2['Query_pheno']>=df2['Proxy_pheno'],df2['Query_pheno'],'0')

df2=df2.drop(['Query_pheno','Proxy_pheno'], axis = 1)

df2.to_csv("/home/saikat/Heterogeneous_diabetes/query_proxy_test1.csv", sep='\t', index=False)

a=df2.to_numpy()

query_proxy_temp=[]
seen=set()

with open("/home/saikat/Heterogeneous_diabetes/diabetes2_plink.ped",'w') as out:
    for i in range(len(a)):
        out.write("%s %s %s %s %s %s %s %s %s %s\n"%('F'+str(i+1),'I'+str(i+1),'0','0','0',a[i][6],a[i][2],a[i][3],a[i][4],a[i][5]))
        if a[i][0] not in seen:
            seen.add(a[i][0])
            query_proxy_temp.append(a[i][0])
        if a[i][1] not in seen:
            seen.add(a[i][1])
            query_proxy_temp.append(a[i][0])
        else:
            pass

temp=set()
diabetes2_var_vep=[]        
with open("/home/saikat/Heterogeneous_diabetes/diabetes_var_parse_final.txt") as f:
    for line in f:
        ind=line.strip('\n').split('\t')
        if (ind[0],ind[1],ind[2]) not in seen:
            seen.add((ind[0],ind[1],ind[2]))
            diabetes2_var_vep.append((ind[0],ind[1],ind[2]))
        else:
            pass
        
df3=pd.DataFrame(diabetes2_var_vep,index=None)

b=df3.to_numpy()

tripple=set()

with open("/home/saikat/Heterogeneous_diabetes/diabetes2_plink.map",'w') as out:
    for v in query_proxy_temp:
        for i in range(len(b)):
            if v==b[i][1]:
                if (b[i][0],b[i][1],b[i][2]) not in tripple:
                    tripple.add((b[i][0],b[i][1],b[i][2]))
                    out.write("%s\t%s\t%s\n"%(b[i][0],b[i][1],b[i][2]))
                else:
                    pass
            else:
                pass
        
        



        


