#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 21:39:00 2021

@author: saikat
"""

import pandas as pd

file = open("/home/saikat/Heterogeneous_diabetes/diabetes2_plink.ped","r")
Counter = 0
  
# Reading from file
Content = file.read()
CoList = Content.split("\n")
  
for i in CoList:
    if i:
        Counter += 1

ped_temp=[[] for k in range(Counter)]

c=0
with open("/home/saikat/Heterogeneous_diabetes/diabetes2_plink.ped") as f:
    for line in f:
        ind=line.strip('\n').split()
        i=0
        while i<=9:
            ped_temp[c].append(ind[i])
            i+=1
        c+=1

x='0'
        
for i in range(c):
    ped_temp[i].extend([x for j in range(2867)])
    
    
df1=pd.DataFrame(ped_temp,index=None)
# nquery_header=df1.iloc[0]        
# df1=df1[1:]
# df1=nquery_header

df1.to_csv("/home/saikat/Heterogeneous_diabetes/diabetes2_plink_ped.ped", sep=' ',index=False,header=False)