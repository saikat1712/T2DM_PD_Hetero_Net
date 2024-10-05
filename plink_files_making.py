#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 10:55:42 2021

@author: saikat
"""

import pandas as pd 


query_proxy=[]
query=[]
proxy=[]

with open("/home/saikat/diabetes/diabetes2_SNP_Proxy/final_diabetes2_proxys.txt") as f:
    for line in f:
        ind=line.strip('\n').split('\t')
        if ind[0]!=ind[1]:
            query_proxy.append((ind[0],ind[1]))
            query.append(ind[0])
            proxy.append(ind[1])
        else:
            pass
        
df1= pd.DataFrame(query_proxy,index=None)   
n1_header=df1.iloc[0]        
df1=df1[1:]
df1.columns=n1_header

df_query= pd.DataFrame(query,index=None)   ############### query RSID
n11_header=df_query.iloc[0]        
df_query=df_query[1:]
df_query.columns=n11_header

df_proxy= pd.DataFrame(proxy,index=None)   ################## proxy RSID
n12_header=df_proxy.iloc[0]        
df_proxy=df_proxy[1:]
df_proxy.columns=n12_header




################ making dataframe of the vep list ################

vep_diabetes=[]

vep_diabetes.append(('chr','RSID','BP','ref','alt','pheno'))

with open("/home/saikat/Heterogeneous_diabetes/diabetes_var_parse_final.txt") as f:
    for line in f:
        ind=line.strip('\n').split('\t')
        vep_diabetes.append((ind[0],ind[1],ind[2],ind[3],ind[4],ind[5]))
        
df2= pd.DataFrame(vep_diabetes,index=None)   
n2_header=df2.iloc[0]        
df2=df2[1:]
df2.columns=n2_header

df3= df_query.rename(columns={'QRSID':'RSID'})

new_df_query=pd.merge(df3, df2, how='inner',on=['RSID'])

new_df_query=new_df_query.drop_duplicates()

new_df_query= new_df_query.rename(columns= {'RSID':'Query_RSID','pheno':'Query_pheno','chr':'Query_chr','BP':'Query_BP','ref':'Query_ref','alt':'Query_alt'})

new_df_query.to_csv("/home/saikat/Heterogeneous_diabetes/query_vep.csv", sep="\t",index=False)


new_df_proxy=pd.merge(df_proxy, df2, how='inner',on=['RSID'])    

new_df_proxy=new_df_proxy.drop_duplicates() 

new_df_proxy= new_df_proxy.rename(columns={'RSID':'Proxy_RSID','pheno':'Proxy_pheno','chr':'Proxy_chr','BP':'Proxy_BP','ref':'Proxy_ref','alt':'Proxy_alt'})

new_df_proxy.to_csv("/home/saikat/Heterogeneous_diabetes/proxy_vep.csv", sep="\t",index=False)   



query_proxy_variants=[]
vep_values=set()

a=new_df_query.to_numpy()
b=new_df_proxy.to_numpy()

for k1,k2 in query_proxy:
    for i in range(len(a)):
        if a[i][0] == k1:
            for j in range(len(b)):
                if b[j][0] == k2:
                    if (a[i][0],b[j][0],a[i][3],a[i][4],b[j][3],b[j][4],a[i][5],b[j][5]) not in vep_values:
                        vep_values.add((a[i][0],b[j][0],a[i][3],a[i][4],b[j][3],b[j][4],a[i][5],b[j][5]))
                        query_proxy_variants.append((a[i][0],b[j][0],a[i][3],a[i][4],b[j][3],b[j][4],a[i][5],b[j][5]))
                    else:
                        pass
                else:
                    pass
        else:
            pass
        
        
df_query_proxy= pd.DataFrame(query_proxy_variants,index=None)   
nquery_pair_header=df_query_proxy.iloc[0]        
df_query_proxy=df_query_proxy[1:]
df_query_proxy.columns=nquery_pair_header


df_query_proxy.to_csv("/home/saikat/Heterogeneous_diabetes/query_proxy_info.txt",sep='\t',index=False)

df_query_proxy.to_csv("/home/saikat/Heterogeneous_diabetes/query_proxy_info.csv",sep='\t',index=False)



                
        
    
        
        
        
    
    