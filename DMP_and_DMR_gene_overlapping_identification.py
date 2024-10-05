# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 08:06:30 2021

@author: ASUS
"""

import pandas as pd


# df_dmp= pd.read_csv(r'D:\Epigenomic_proj\diabetes_methylation_GSE65057\_all_DMPs.csv')

# # print(df_dmp)

# df1= df_dmp.iloc[:,[3,0,11,12,14,22,25,27]]

# df1.to_csv(r'D:\Epigenomic_proj\diabetes_methylation_GSE65057\DMPs_with_desired_columns.csv',mode = 'w', index=False) 


df_dmr= pd.read_csv(r'D:\Epigenomic_proj\diabetes_methylation_GSE65057\All_DMR.csv', sep='delimeter', engine='python')

# foo = lambda x: pd.Series([i for i in reversed(x.split(','))])
# df2 = df_dmr[',seqnames,start,end,width,strand,no.cpgs,min_smoothed_fdr,Stouffer,HMFDR,Fisher,maxdiff,meandiff,overlapping.genes'].apply(foo)

df2=df_dmr[',seqnames,start,end,width,strand,no.cpgs,min_smoothed_fdr,Stouffer,HMFDR,Fisher,maxdiff,meandiff,overlapping.genes'].apply(lambda x: pd.Series(x.split(',')))


# print(df2)

df2.to_csv(r'D:\Epigenomic_proj\diabetes_methylation_GSE65057\DMRs_with_desired_columns.csv',mode = 'w', index=False)