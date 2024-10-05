# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 07:28:44 2021

@author: ASUS
"""

gwas_snp=[]

import re
import pandas as pd


        
df=pd.read_csv('/home/saikat/SNP_GWAS_dataset/gwas_catalog_v1.0.2-associations_e100_r2020-12-15.tsv', sep='\t', encoding="utf8", low_memory=False)        
df.to_csv("/home/saikat/Epigenomic_proj/gwas_snp_parsed.csv",index=False)

df1=df[['MAPPED_TRAIT','SNPS','P-VALUE','CONTEXT','REPLICATION SAMPLE SIZE']]
df11=df1.loc[df1['MAPPED_TRAIT']=="Parkinson's disease"]
df11.to_csv("/home/saikat/Epigenomic_proj/gwas_snp_parsed_Parkinson.csv",index=False, header=False)
df_diab=df11[['SNPS']]
l= df_diab['SNPS'].tolist()



with open("/home/saikat/Epigenomic_proj/Parkinson_snps_temp.txt", 'w') as out:
          for k in l:
              if k.startswith('rs') == True:
                  out.write("%s\n"%k)
              else:
                  pass
              
temp=[]

with open("/home/saikat/Epigenomic_proj/Parkinson_snps_temp.txt") as f:
    for line in f:
        ind=line.strip('\n')
        # print(ind[0])
        if bool(re.search('x', ind))== False and bool(re.search(';', ind))== False:
            temp.append(ind)
        if 'x' in ind:
            y1= re.findall('([^ x]+)',ind)
            temp.append(y1[0])
            temp.append(y1[1])            
        if ';' in ind:
            y2= re.findall('([^ ;]+)',ind)
            for i in range(len(y2)):
                temp.append(y2[i])
        else:
            pass
        
# print(len(temp))
        
final= list(set(temp))

with open("/home/saikat/Epigenomic_proj/Parkinson_snps.txt",'w') as out:
    for v in final:
        out.write("%s\n"%v)
        

            
                  
    
