#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 11:55:24 2021

@author: saikat
"""

import pandas as pd
import numpy as np


# #### edge dictionary ######

# edge_type_dict={}

# edge_types=[('pathway','interacts','pathway'),('gene','interacts','gene'),('pathway','interacts','gene'),
#             ('snp','interacts','snp'),('snp','interacts','dmg'),('snp','interacts','ptm'),
#             ('ptm','interacts','ptm'),('amyloid_protein','interacts','amyloid_protein'),('ptm','interacts','amyloid_protein'),
#             ('pathway','interacts','icd'),('amyloid_central_protein','interacts','icd'),
#             ('snp','interacts','icd')]

# i=0
# for k in edge_types:
#     edge_type_dict[k]=i
#     i+=1

## Mapping of Uniprot Genes to their protein names

gene_prots=[]
uniprot_genes=[]

with open("/home/saikat/Epigenomic_proj/uniprot-filtered-organism__Homo+sapiens+(Human)+[9606]_+AND+review--.tab") as f:
    for line in f:
        if line.startswith('Entry')==False:
            ind=line.strip('\n').split('\t')
            gene_prots.append((ind[2],ind[0],ind[1],ind[3]))
            uniprot_genes.append(ind[1])
        

df_uniprot=pd.DataFrame(gene_prots,columns=['Protein','Entry','Gene','Synonym'])
df_uniprot['Gene'] = df_uniprot['Gene'].str.split(';')
df_uniprot = df_uniprot.explode('Gene')
df_uniprot['Synonym']= df_uniprot['Synonym'].str.split(' ')
df_uniprot= df_uniprot.explode('Synonym')
df_uniprot= df_uniprot.drop_duplicates()
# cols=['Gene','Synonym']
# df_uniprot[cols]= df_uniprot[cols].replace('','-9999') ###selecting arbitrary value '-9999' to replace the blank cells
# df_uniprot= df_uniprot[~df_uniprot.select_dtypes(['object']).eq('-9999').any(1)]
### Make two dataframes of prot-gene and prot-synonym and integrate by columnwise fashion
df_uni1= df_uniprot[['Protein','Entry','Gene']]
df_uni2= df_uniprot[['Protein','Entry','Synonym']]
df_uni1= df_uni1.rename(columns={'Gene':'Symbol'})
df_uni2= df_uni2.rename(columns={'Synonym':'Symbol'})
frames= [df_uni1, df_uni2]
final_uniprot= pd.concat(frames) ### concatenation of frames on axis 1 (i.e column wise) 
final_uniprot['Symbol'].replace('',np.nan,inplace=True)
final_uniprot.dropna(subset=['Symbol'],inplace=True)
final_uniprot=final_uniprot.dropna()
final_uniprot=final_uniprot.drop_duplicates()
uniprot_genes=final_uniprot['Symbol'].tolist() 
uniprot_genes=list(set(uniprot_genes))

final_uniprot.to_csv("/home/saikat/Epigenomic_proj/final_uniprot_gene_prots.csv",index=None,header=True)

#### our amyloid_ppi_ptm network #####

ptms=['Methylation','Ubiquitination','Amidation','Hydroxylation','O-linked Glycosylation','Phosphorylation','S-nitrosylation','N-linked Glycosylation','Sumoylation','Acetylation','carboxylation','disulfid','oxid','proteolyt'] 
node_node=[]
with open("/home/saikat/Epigenomic_proj/final_amyloid_ppi_ptm_network.txt") as f:
    for line in f:
        ind=line.strip('\n').split('\t')
        node_node.append((ind[0],ind[1]))

node_node_type=[]        
for i in range(len(node_node)):
    if node_node[i][0] in ptms and node_node[i][1] not in ptms:
        node_node_type.append((node_node[i][0],node_node[i][1]))
    if node_node[i][0] not in ptms and node_node[i][1] in ptms:
        node_node_type.append((node_node[i][0],node_node[i][1]))
    if node_node[i][0] in ptms and node_node[i][1] in ptms:
        node_node_type.append((node_node[i][0],node_node[i][1]))
    if node_node[i][0] not in ptms and node_node[i][1] not in ptms:
        node_node_type.append((node_node[i][0],node_node[i][1]))

       
amyloid_df=pd.DataFrame(node_node_type,columns=['node1','node2'])

uniprot_dict=dict(zip(final_uniprot.Symbol,final_uniprot.Entry))

## only map column values if that exists in the dictionary keys, else it will unchanged ###
amyloid_df.loc[amyloid_df['node1'].isin(uniprot_dict.keys()),'node1']=amyloid_df['node1'].map(uniprot_dict) 
amyloid_df.loc[amyloid_df['node2'].isin(uniprot_dict.keys()),'node2']=amyloid_df['node2'].map(uniprot_dict)


amyloid_df.to_csv("/home/saikat/Epigenomic_proj/final_amyppi_ptm_network_with_uniprot_id.csv",index=None)

## mapping central protein - icdE11.8 interactions

central_icd=[]
with open("/home/saikat/Epigenomic_proj/Amyloid_central_prot_to_ICD-10_E11.8.txt") as f:
    for line in f:
        ind=line.strip('\n').split('\t')
        central_icd.append((ind[0],ind[1]))
central_icd_df=pd.DataFrame(central_icd,columns=['entity1','entity2']) 
 
## creating multivalued dictionary and mapping to the central proteins to uniprot ids

final_uniprot=final_uniprot.dropna()
uni_dict_same=final_uniprot[['Symbol','Entry']]
uni_dict_same.set_index('Symbol',inplace=True)
uni_dict_same=uni_dict_same.to_dict()['Entry']
central_icd_df.loc[central_icd_df['entity1'].isin(uni_dict_same.keys()),'entity1']=central_icd_df['entity1'].map(uni_dict_same) 
df1 = central_icd_df[~central_icd_df['entity1'].isin(uni_dict_same.values())]
central_icd_df = central_icd_df.drop(df1.index)
central_icd_df=central_icd_df.reset_index().drop(columns=['index'])

## selecting entities only contains in amyloid_ppi_ptm_network 

combined_amy=amyloid_df
combined_amy['entity1']=combined_amy['node1'].append(combined_amy['node2']).reset_index(drop=True)
combined_amy=combined_amy.drop(columns=['node1','node2'])

central_icd_df_final=pd.merge(central_icd_df,combined_amy,how='inner',on=['entity1'])
central_icd_df_final=central_icd_df_final.drop_duplicates().reset_index().drop(columns=['index'])

central_icd_df_final.to_csv("/home/saikat/Epigenomic_proj/Amyloid_central_id_to_ICD-10_E11.8.csv",index=None)
  
    
        