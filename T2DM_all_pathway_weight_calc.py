#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 29 23:33:46 2021

@author: saikat
"""
import re
import pandas as pd
import numpy as np


### Extacting color module names

modules=[]
with open("/localhome/pabitra/diabetes_path_path_weight/modcolor_node_files.txt") as f:
    for line in f:
        ind=line.strip('\n')
        y=re.findall('([a-z0-9A-Z]+)',ind)
        modules.append(y[2])

# modules=['darkred','bisque4']
        
        
#### combining similar color module files

from os import listdir

# dis_files=[[] for i in range(len(modules))]

dis_files=[[] for i in range(len(modules))]

path='/localhome/pabitra/diabetes_path_path_weight/'

def pathway_weight_cal(fname,n):
    path_path=[]
    if "score" in fname[0]:        
        with open(fname[0]) as f:
            for line in f:
                ind=line.strip('\n').split('\t')
                if ind[0]!=ind[1]:
                    path_path.append((ind[0],ind[1],ind[2]))
                else:
                    pass
    if "score" in fname[1]:
        with open(fname[1]) as f:
            for line in f:
                ind=line.strip('\n').split('\t')
                if ind[0]!=ind[1]:
                    path_path.append((ind[0],ind[1],ind[2]))
                else:
                    pass
    
    path_path_df=pd.DataFrame(path_path,index=None,columns=['pathway1','pathway2','semantic_score'])
    
    pheno_info=[] 
    
    if "mutual" in fname[1]:
        with open(fname[1]) as f:
            for line in f:
                ind=line.strip('\n').split('\t')
                pheno_info.append((ind[0],ind[1]))
    if "mutual" in fname[0]:
        with open(fname[0]) as f:
            for line in f:
                ind=line.strip('\n').split('\t')
                pheno_info.append((ind[0],ind[1]))
            
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
    
    path_df_with_semantic_pheno.to_csv(r"/localhome/pabitra/diabetes_path_path_weight/sem_pheno_modules/path_path_{}_sem_pheno.csv".format(n),sep=',',index=None,header=True) 
    
    


i=0
for n in modules:
    for filename in listdir("/localhome/pabitra/diabetes_path_path_weight"):
        if n in filename:
            dis_files[i].append(path+filename)
        else:
            pass
    pathway_weight_cal(dis_files[i],n)
        
    i+=1
    



    
        
