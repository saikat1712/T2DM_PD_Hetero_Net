#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 21:18:03 2021

@author: saikat
"""

import pandas as pd
import re


from os import listdir

def genecoexpression_overlaps(df,n):
    path='/home/saikat/diabetes/gene_coexpression_subnetworks/'
    for fname in listdir("/home/saikat/diabetes/gene_coexpression_subnetworks"):
        if fname.startswith("CytoscapeInput_nodes_")==True and fname.endswith(".csv")==True:
            y2=re.findall('([^_.]+)',fname)
            if y2[2]==n:
                df_nodes=pd.read_csv(path+fname,sep='\t')
                df_nodes=df_nodes.drop(columns=['altName','nodeAttr[nodesPresent, ]'])
                df_nodes=df_nodes.rename(columns={'nodeName':'gene_symbol'})
                df_module_asso=pd.merge(df_nodes, df, how='inner',on=['gene_symbol'])
                df_module_asso.to_csv(r"/home/saikat/diabetes/genecoexpression_specific_path_gene_associations/coexpresion_specific_path_gene_{}_association.csv".format(n),sep=',',index=None,header=True)
            else:
                pass

path='/home/saikat/diabetes/T2DM_path_gene_dfs/'
for filename in listdir("/home/saikat/diabetes/T2DM_path_gene_dfs"):
    if filename.endswith(".csv")==True:
        y1=re.findall('([^_.]+)',filename) ## retrieving the module color
        df_t=pd.read_csv(path+filename)
        df_t=df_t.applymap(lambda x: x.replace('"', '')) ## for remving double quotes
        df_t['gene_symbol']=df_t['gene_symbol'].str.split('\s+')
        df_f=df_t.explode('gene_symbol').replace('"','')
        genecoexpression_overlaps(df_f,y1[5])
        df_f.to_csv(r"/home/saikat/diabetes/T2DM_path_gene_dfs/modulepath_gene_associations/modulepath_gene_{}_association.csv".format(y1[5]),sep=',',index=None,header=True) 
    else:
        pass

    
 
## searching through the gene-coexpression input nodes




        
        
    
            

