#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 10:48:11 2021

@author: saikat
"""

import re

import pandas as pd

seen=set()


with open("/home/saikat/Desktop/diabetes2_variants_out_final.txt") as f,open("/home/saikat/Heterogeneous_diabetes/diabetes_var_parse.txt",'w') as out:
    for line in f:
        if line.startswith('#') == False:
            ind=line.strip('\n').split('\t')
            if ind[1].startswith('CHR_') == False:
                if (ind[0],ind[1],ind[2],ind[3],ind[4],ind[7]) not in seen:
                    seen.add((ind[0],ind[1],ind[2],ind[3],ind[4],ind[7]))
                    out.write("%s\t%s\t%s\t%s\t%s\t%s\n"%(ind[0],ind[1],ind[2],ind[3],ind[4],ind[7]))
                else:
                    pass
            else:
                pass
        else:
            pass
        
diabetes_map=[]

values_all=set()

diabetes_map.append(('chr','RSID','BP','ref','alt','gene_id','pheno'))

with open("/home/saikat/Heterogeneous_diabetes/diabetes_var_parse.txt") as f,open("/home/saikat/Heterogeneous_diabetes/diabetes_var_parse_final.txt",'w') as out:
    for line in f:
        ind=line.strip('\n').split('\t')
        y=re.findall('([^ :]+)',ind[1])
        if ind[5]=='-' and (y[0],ind[0],y[1],ind[3],ind[2],ind[4],'1') not in values_all:
            diabetes_map.append((y[0],ind[0],y[1],ind[3],ind[2],ind[4],'1'))
            values_all.add((y[0],ind[0],y[1],ind[3],ind[2],ind[4],'1'))
            out.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(y[0],ind[0],y[1],ind[3],ind[2],ind[4],'1'))
        elif ind[5]!='-' and (y[0],ind[0],y[1],ind[3],ind[2],ind[4],'2') not in values_all:
            diabetes_map.append((y[0],ind[0],y[1],ind[3],ind[2],ind[4],'2'))
            values_all.add((y[0],ind[0],y[1],ind[3],ind[2],ind[4],'2'))
            out.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(y[0],ind[0],y[1],ind[3],ind[2],ind[4],'2'))
        else:
            pass

df1= pd.DataFrame(diabetes_map,index=None)   
n1_header=df1.iloc[0]        
df1=df1[1:]
df1.columns=n1_header
 
# ########## parsing the GTEx_liver data #################################
liver_gtx=[]

liver_gtx.append(('gene_id','MAF'))

with open("/home/saikat/Datasets/GTEx_Analysis_v8_eQTL/Liver.v8.EUR.egenes.txt") as f:
    for line in f:
        if line.startswith('phenotype_id')==False:
            ind=line.strip('\n').split('\t')
            if ind[10]>=str(0.05):
                y1=re.findall('([^ .]+)',ind[0])
                liver_gtx.append((y1[0],ind[10]))
            else:
                pass
        else:
            pass
        
df2= pd.DataFrame(liver_gtx)
n2_header=df2.iloc[0]        
df2=df2[1:]
df2.columns=n2_header

# # #################### mapping to the ensembl-vep rsid of diabetes GTEx data ######################################

new_df= pd.merge(df1,df2,how='inner',on=['gene_id'])

new_df.dropna(inplace=True)

new_df.to_csv('/home/saikat/Heterogeneous_diabetes/gtx_Eur_liver_rsids_only.txt',sep='\t',mode='a',index=False)
new_df.to_csv('/home/saikat/Heterogeneous_diabetes/gtx_Eur_liver_rsids_only.csv',sep=',',mode='a',index=False)



            
        
           
            
        