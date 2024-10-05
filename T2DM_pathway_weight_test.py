#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 28 21:57:30 2021

@author: saikat
"""
import pandas as pd
import numpy as np

path_path=[]

with open("/home/saikat/T2DM_test/path_path_score_bisque4.txt") as f:
    for line in f:
        ind=line.strip('\n').split('\t')
        if ind[0]!=ind[1]:
            path_path.append((ind[0],ind[1],ind[2]))
        else:
            pass

path_path_df=pd.DataFrame(path_path,index=None,columns=['pathway1','pathway2','semantic_score'])

# path_path_arr=path_path_df.to_numpy()   

# path_path_df[['pathway1','pathway2','semantic_score']]=path_path_df

pheno_info=[]  
paths=[]      
with open("/home/saikat/T2DM_test/phenotype_mutual_information_nodes_bisque4.txt") as f:
    for line in f:
        ind=line.strip('\n').split('\t')
        pheno_info.append((ind[0],ind[1]))
        # paths.append(ind[0])
        
arr_l=len(pheno_info)
    
path_info_arr=np.reshape(np.asarray(pheno_info), (arr_l,2))
        
#### Mutual info selection calculation

path_pair_entropy=[]

seen=set()

for i in range(arr_l):
    for j in range(arr_l):
        Wavg= float((float(path_info_arr[i][1])+float(path_info_arr[j][1]))/2)
        max1=max(float(path_info_arr[i][1]),Wavg)
        max2=max(float(path_info_arr[j][1]),Wavg)
        fmax=max(max1,max2)
        if (path_info_arr[i][0],path_info_arr[j][0],fmax) not in seen:
            seen.add((path_info_arr[i][0],path_info_arr[j][0],fmax))
            path_pair_entropy.append((path_info_arr[i][0],path_info_arr[j][0],fmax))
        else:
            pass
            
path_pair_entropy_df=pd.DataFrame(path_pair_entropy,index=None,columns=['pathway1','pathway2','phenotype_entropy'])

path_df_with_semantic_pheno=pd.merge(path_path_df, path_pair_entropy_df, how='inner',on=['pathway1','pathway2']) 

path_df_with_semantic_pheno["semantic_score"]= path_df_with_semantic_pheno["semantic_score"].astype(float)

path_df_with_semantic_pheno["phenotype_entropy"]= path_df_with_semantic_pheno["phenotype_entropy"].astype(float)

sum_col= path_df_with_semantic_pheno["semantic_score"] + path_df_with_semantic_pheno["phenotype_entropy"]

path_df_with_semantic_pheno["Edge_weight"]=sum_col

path_df_with_semantic_pheno.to_csv("/home/saikat/T2DM_test/path_path_bisque4_sem_pheno.csv",sep=',',index=None,header=True) 

