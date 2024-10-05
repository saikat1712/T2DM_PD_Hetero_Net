#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 16:45:59 2021

@author: saikat
"""

from os import listdir
import pandas as pd
import re
import networkx as nx


path='/home/saikat/diabetes/sem_pheno_modules/'
for filename in listdir("/home/saikat/diabetes/sem_pheno_modules"):
    y=re.findall('([^_.]+)',filename)
    df_t=pd.read_csv(path+filename)
    df_mod=df_t[['pathway1','pathway2','Edge_weight']]
    G=nx.Graph()
    G=nx.from_pandas_edgelist(df_mod,'pathway1','pathway2',['Edge_weight'])
    dc=nx.pagerank(G)
    df2=pd.DataFrame.from_dict({'node':list(dc.keys()),'centrality':list(dc.values())})
    df2=df2.sort_values('centrality',ascending=False)
    col_val=df2["centrality"]
    max_val=col_val.max()
    df2=df2.loc[df2["centrality"] >= max_val]
    df2=df2.drop(columns=['centrality'])
    df2['ICD']='E11.8'
    df2.to_csv(r"/home/saikat/diabetes/pathway_to_ICD_for_each_modules/path_{}_ICD_E11.8_association.csv".format(y[2]),sep=',',index=None,header=True)

    