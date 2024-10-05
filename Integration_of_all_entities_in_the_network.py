#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 20:02:00 2021

@author: saikat
"""
## Integrating all entities from the individual subnetworks

from __future__ import print_function
from os import listdir
import os, os.path
import pandas as pd
import  re
import numpy as np

## Making dictionary of node_types

node_type_dict={}

node_types = ['pathway','downregulated_gene','upregulated_gene','hypo_methylated_gene',
              'hyper_methylated_gene','downregulated_hyper_methylated_gene',
              'upregulated_hyper_methylated_gene','downregulated_hypo_methylated_gene','upregulated_hypo_methylated_gene',
              'gene','rsid_snp','amyloid_protein','central_amyloid_protein_t2dm_E11.8',
              'ptm']

i=0
for k in node_types:
    node_type_dict[k]=i
    i+=1

## All Pathways integrated list

path='/home/saikat/diabetes/sem_pheno_modules/'

# path, dirs, files = next(os.walk(path1))
# l = len(files)

paths=[]
for filename in listdir("/home/saikat/diabetes/sem_pheno_modules"):
    df_path=pd.read_csv(path+filename)
    path1=df_path['pathway1'].tolist()
    path2=df_path['pathway2'].tolist()
    paths=paths+path1+path2    

all_paths=list(set(paths))

pathways_df= pd.DataFrame(all_paths, columns=['entity'])
pathways_df['entity_concept']= pathways_df['entity']
pathways_df['entity_type_id'] = node_type_dict['pathway']
pathways_df['entity_type'] = 'pathway'
# df_pathways.to_csv("/home/saikat/diabetes/final_all_path_entities_with_concept.csv",index=None)

## All Genes integrated list
genes=[]

path='/home/saikat/diabetes/gene_coexpression_subnetworks/'
for fname in listdir('/home/saikat/diabetes/gene_coexpression_subnetworks'):
    if fname.startswith('CytoscapeInput_edges_') and fname.endswith('.csv'):
        df_g=pd.read_csv(path+fname,sep='\t')
        df_g=df_g[['fromNode','toNode']]
        genes_l=df_g['fromNode'].tolist() + df_g['toNode'].tolist()
        genes=genes+genes_l
    else:
        pass
    
all_mod_genes=list(set(genes))

with open('/home/saikat/diabetes/genes_test.txt','w') as out:
    for a in all_mod_genes:
        out.write("%s\n"%a)

## UP/DOWN REGULATED GENES (DEGs)

df_up= pd.read_csv('/home/saikat/Heterogeneous_diabetes/diabetes_2_Methylation_overlap/UP_Regulated_DEGs.csv')
up_regul=df_up['SYMBOL'].tolist()
up_regul=list(set(up_regul).intersection(set(all_mod_genes)))

df_down= pd.read_csv('/home/saikat/Heterogeneous_diabetes/diabetes_2_Methylation_overlap/DOWN_Regulated_DEGs.csv')
down_regul=df_down['SYMBOL'].tolist()
down_regul=list(set(down_regul).intersection(set(all_mod_genes)))


## Hypo and Hypermethylated Genes 

df_hyper= pd.read_csv("/home/saikat/Heterogeneous_diabetes/diabetes_2_Methylation_overlap/Hypermethylated_DEGs_with_GO_enriched.csv")

try:
    df_hyper_genes=df_hyper['Hypermethylated_DEGs'] + '_' + df_hyper['GO_term'] + '_hypermethylated'
    hyper=df_hyper['Hypermethylated_DEGs'].tolist()
    hyper=list(set(hyper).intersection(set(all_mod_genes)))
    # hyper_genes=df_hyper_genes.tolist()
except ValueError:
    hyper=[]
    hyper_append=[]

df_hypo= pd.read_csv("/home/saikat/Heterogeneous_diabetes/diabetes_2_Methylation_overlap/Hypomethylated_DEGs_with_GO_enriched.csv")

try:
    df_hypo_genes=df_hypo['Hypomethylated_DEGs'] + '_' + df_hypo['GO_term'] + ' _hypomethylated'
    hypo=df_hypo['Hypomethylated_DEGs'].tolist()
    hypo=list(set(hypo).intersection(set(all_mod_genes)))
    # hypo_genes=df_hypo_genes.tolist()
except ValueError:
    hypo=[]
    hyper_append=[]


## UP/DOWN regulated and hyper/hypo methylated genes

# DOWNREGULATED + HYPERMETHYLATED CHECK
if len(hyper) !=0 :
    down_hyper= list(set(hyper).intersection(set(down_regul)))
    down_hyper_df= pd.DataFrame(down_hyper,columns=['entity'])
    down_hyper_df['entity_concept']= down_hyper_df['entity']
    down_hyper_df['entity_type_id']=node_type_dict['downregulated_hyper_methylated_gene']
    down_hyper_df['entity_type'] = 'downregulated_hyper_methylated_gene'

else:
    down_hyper=[]
    down_hyper_df=pd.DataFrame(columns=['entity','entity_concept','entity_type_id','entity_type'])
    
    
# UPREGULATED + HYPERMETHYLATED CHECK  
if len(hyper) !=0 :
    up_hyper= list(set(hyper).intersection(set(up_regul)))
    up_hyper_df= pd.DataFrame(up_hyper,columns=['entity'])
    up_hyper_df['entity_concept']= up_hyper_df['entity']
    up_hyper_df['entity_type_id']=node_type_dict['upregulated_hyper_methylated_gene']
    up_hyper_df['entity_type'] = 'upregulated_hyper_methylated_gene'
else:
    up_hyper=[]
    up_hyper_df=pd.DataFrame(columns=['entity','entity_concept','entity_type_id','entity_type'])
    
    
# DOWNREGULATED + HYPOMETHYLATED CHECK    
if len(hypo) !=0 :
    down_hypo= list(set(hypo).intersection(set(down_regul)))
    down_hypo_df= pd.DataFrame(down_hypo,columns=['entity'])
    down_hypo_df['entity_concept']= down_hypo_df['entity']
    down_hypo_df['entity_type_id']=node_type_dict['downregulated_hypo_methylated_gene']
    down_hypo_df['entity_type'] = 'downregulated_hypo_methylated_gene'
else:
    down_hypo_df=pd.DataFrame(columns=['entity','entity_concept','entity_type_id','entity_type'])
    
    
# UPREGULATED + HYPOMETHYLATED CHECK    
if len(hypo) !=0 :
    up_hypo= list(set(hypo).intersection(set(up_regul)))
    up_hypo_df= pd.DataFrame(up_hypo,columns=['entity'])
    up_hypo_df['entity_concept']= up_hypo_df['entity']
    up_hypo_df['entity_type_id']=node_type_dict['upregulated_hypo_methylated_gene']
    up_hypo_df['entity_type'] = 'upregulated_hypo_methylated_gene'

else:
    up_hypo_df=pd.DataFrame(columns=['entity','entity_concept','entity_type_id','entity_type'])
    

    
## only Hypermethylated genes

only_hyper= list(set(hyper)-set(up_hyper+down_hyper))

if len(only_hyper)!=0:
    only_hyper_df= pd.DataFrame(only_hyper, columns=['entity'])
    only_hyper_df['entity_concept']= only_hyper_df['entity']
    only_hyper_df['entity_type_id']=node_type_dict['hyper_methylated_gene']
    only_hyper_df['entity_type'] = 'hyper_methylated_gene'
else:
    only_hyper_df=pd.DataFrame(columns=['entity','entity_concept','entity_type_id','entity_type'])

## only Hypomethylated genes

only_hypo= list(set(hypo)-set(up_hypo+down_hypo))

if len(only_hypo)!=0:
    only_hypo_df= pd.DataFrame(only_hypo, columns=['entity'])
    only_hypo_df['entity_concept']= only_hypo_df['entity']
    only_hypo_df['entity_type_id']=node_type_dict['hypo_methylated_gene']
    only_hypo_df['entity_type']= 'hypo_methylated_gene'
else:
    only_hypo_df=pd.DataFrame(columns=['entity','entity_concept','entity_type_id','entity_type'])

## only Upregulated genes

only_up_regul= list(set(up_regul)-set(up_hyper+up_hypo))

if len(only_up_regul)!=0:
    only_up_regul_df= pd.DataFrame(only_up_regul, columns=['entity'])
    only_up_regul_df['entity_concept']= only_up_regul_df['entity']
    only_up_regul_df['entity_type_id']=node_type_dict['upregulated_gene']
    only_up_regul_df['entity_type'] = 'upregulated_gene'
else:
    only_up_regul_df=pd.DataFrame(columns=['entity','entity_concept','entity_type_id','entity_type'])

## only Downregulated genes

only_down_regul= list(set(down_regul)-set(down_hyper+down_hypo))

if len(only_down_regul)!=0:
    only_down_regul_df= pd.DataFrame(only_down_regul, columns=['entity'])
    only_down_regul_df['entity_concept']= only_down_regul_df['entity']
    only_down_regul_df['entity_type_id']=node_type_dict['downregulated_gene']
    only_down_regul_df['entity_type'] = 'downregulated_gene'
else:
    only_down_regul_df=pd.DataFrame(columns=['entity','entity_concept','entity_type_id','entity_type'])


## only genes excluding Upregulated/Downregulated and Hypermethylated/Hypomethylated genes

only_genes= list(set(all_mod_genes)-set(only_up_regul+only_down_regul+only_hyper+only_hypo+up_hypo+down_hypo+up_hyper+down_hyper))
only_genes_df= pd.DataFrame(only_genes,columns=['entity'])
only_genes_df['entity_concept']= only_genes_df['entity']
only_genes_df['entity_type_id']=node_type_dict['gene']
only_genes_df['entity_type'] = 'gene'
## All SNPs (RSIDs) integration

df_snp=pd.read_csv("/home/saikat/diabetes/plink.epi.cc.txt",sep='\s+')

s1=list(df_snp.SNP1)
s2=list(df_snp.SNP2)
        
all_snps=list(set(s1+s2))

vep_temp=[]
with open("/home/saikat/diabetes/diabetes2_variants_out_final.txt") as f:
    for line in f:
        if line.startswith('#')==False:
            ind=line.strip('\n').split('\t')
            vep_temp.append((ind[0],ind[6]))
        else:
            pass
        
df_T2DM_vep=pd.DataFrame(vep_temp,columns=['RSID','Type'])

df_all_RSID=pd.DataFrame(all_snps,columns=['RSID'])

df_RSID_vep= pd.merge(df_all_RSID,df_T2DM_vep,how='inner',on=['RSID'])
df_RSID_vep=df_RSID_vep.drop_duplicates()
            
df_RSID_vep=df_RSID_vep.groupby('RSID')['Type'].apply(' '.join).reset_index()

df_RSID_vep['entity_concept']= df_RSID_vep['RSID'] + ' ' + df_RSID_vep['Type']

RSIDs_df= df_RSID_vep.drop(columns=['Type'])
RSIDs_df=RSIDs_df.rename(columns={'RSID':'entity'})
RSIDs_df['entity_type_id']=node_type_dict['rsid_snp']
RSIDs_df['entity_type'] = 'rsid_snp'

# all_RSIDs= df_RSIDs.tolist()


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
final_uniprot=final_uniprot[['Entry','Protein']]

final_uniprot.to_csv("/home/saikat/Epigenomic_proj/final_uniprot_gene_prots.csv",index=None,header=True)
        
## Union of amyloid_protein entities

df_amynet=pd.read_csv("/home/saikat/Epigenomic_proj/final_amyppi_ptm_network_with_uniprot_id.csv")
all_amynet_entities= list(set(df_amynet['node1'].tolist()+df_amynet['node2'].tolist()))

df_amynet_entity=pd.DataFrame(all_amynet_entities,columns=['Entry'])

df_amynet_merge=pd.merge(df_amynet_entity,final_uniprot,how='inner', on=['Entry'])
df_amynet_merge=df_amynet_merge.dropna()
df_amynet_merge= df_amynet_merge.drop_duplicates()
df_amynet_merge= df_amynet_merge.groupby('Entry')['Protein'].apply(' '.join).reset_index()
df_amynet_merge.to_csv("/home/saikat/Epigenomic_proj/amyloid_network_prots.csv",index=None)
merge_genes= df_amynet_merge['Entry'].tolist()
all_amyloid_prots_df= df_amynet_merge
all_amyloid_prots_df= all_amyloid_prots_df.rename(columns={'Entry':'entity','Protein':'entity_concept'})
all_amyloid_prots_df['entity_type_id']=node_type_dict['amyloid_protein']
all_amyloid_prots_df['entity_type']='amyloid_protein'
all_amyloid_prots_final_df = all_amyloid_prots_df

## only invitro-invivo amyloid central proteins and subsetting them from all_amyloid_prots_df
final_uni_other = final_uniprot ## uniprot proteins and their corresponding description 
final_uni_other = final_uni_other.rename(columns={'Entry':'entity','Protein':'entity_concept'})
central_prot_df = pd.read_csv("/home/saikat/Epigenomic_proj/Amyloid_central_id_to_ICD-10_E11.8.csv")
central_prot_df = central_prot_df.drop(columns=['entity2'])
central_prot_df = central_prot_df.rename(columns={'entity1':'entity'})
central_prot_df = pd.merge(central_prot_df,final_uni_other,how='inner',on=['entity'])
central_prot_df = central_prot_df.drop_duplicates()
## merging the rows with similar column values using groupby() 
central_prot_df = central_prot_df.groupby(central_prot_df['entity'])['entity_concept'].apply(';'.join).reset_index()
central_prot_df['entity_concept'] = central_prot_df['entity_concept'] + ' ' + 'amyloid precursor central protein'
central_prot_final_df = central_prot_df
central_prot_final_df['entity_type_id'] = node_type_dict['central_amyloid_protein']
central_prot_final_df['entity_type'] = 'central_amyloid_protein'

## Taking only those central proteins, which are present in the amyloid network

all_amyloid_prots = all_amyloid_prots_final_df['entity'].tolist()

central_prot_final_df = central_prot_final_df[central_prot_final_df['entity'].isin(all_amyloid_prots)]

central_prot_final_df = central_prot_final_df.reset_index(drop=True)

## eleminating central amyloids from all amyloids

central_amy_proteins = central_prot_final_df['entity'].tolist()
all_amyloid_prots_final_df = all_amyloid_prots_final_df[~all_amyloid_prots_final_df['entity'].isin(central_amy_proteins)]



# Only extracting PTMs

only_ptms= list(set(all_amynet_entities)-(set(all_amynet_entities).intersection(set(merge_genes))))

## PTM concept parsing from UNIPROTKB database

ptm_dict={'Sumoylation':'Sumoylation Post-translational modification', 'Acetylation':'Acetylation Post-translational modification' , 'Amidation':'Amidation Post-translational modification','O-linked Glycosylation':'O-linked Glycosylation Post-translational modification','Ubiquitination': 'Ubiquitination Post-translational modification','Hydroxylation':'Hydroxylation Post-translational modification','S-nitrosylation':'S-nitrosylation Post-translational modification', 'Phosphorylation':'Phosphorylation Post-translational modification', 'oxid':'Oxidative Post-translational modification','disulfid':'Disulfide bond Post-translational modification', 'N-linked Glycosylation':'N-linked Glycosylation Post-translational modification', 'Methylation':'Methylation Post-translational modification', 'proteolyt':'Proteolytic cleavage Post-translational modification','carboxylation':'Carboxylation Post-translational modification','S-Nitrosylation':'S-Nitrosylation Post-translational modification'}
ptm_df= pd.DataFrame(ptm_dict.items(), columns=['PTM','Concept_ptm'])

amynet_ptm=pd.DataFrame(only_ptms, columns=['PTM'])

## Merging final ptms with their concepts

amynet_ptm_final= pd.merge(amynet_ptm, ptm_df, how='inner', on=['PTM'])

amynet_ptm_final.to_csv("/home/saikat/Epigenomic_proj/final_ptms_with_concept.csv", index=None, header=True)

all_ptms_df= amynet_ptm_final
all_ptms_df= all_ptms_df.rename(columns={'PTM':'entity','Concept_ptm':'entity_concept'})
all_ptms_df['entity_type_id']=node_type_dict['ptm']
all_ptms_df['entity_type'] = 'ptm'

### Making the ICD-10-CM_E11.8 T2DM code mapping to its concept

icd_list= [['E11.8','ICD-10-CM Diagnosis code: E11.8 refers to Type 2 Diabetes Mellitus with unspecified complications']]

icd_df= pd.DataFrame(icd_list, columns=['entity','entity_concept'])
icd_df['entity_type_id']=node_type_dict['icd_t2dm']
icd_df['entity_type'] = 'icd_t2dm'

## Merging all dataframes together

entity_frames=[pathways_df,only_hyper_df,only_hypo_df,only_up_regul_df,only_down_regul_df,down_hyper_df,up_hyper_df,down_hypo_df,up_hypo_df,only_genes_df,RSIDs_df,all_amyloid_prots_final_df,central_prot_final_df,all_ptms_df,icd_df]

final_all_entity_df= pd.concat(entity_frames,ignore_index=True)
final_all_entity_df=final_all_entity_df.dropna()
final_all_entity_df=final_all_entity_df.drop_duplicates()
final_all_entity_df=final_all_entity_df.groupby(['entity','entity_type_id','entity_type'])['entity_concept'].apply(';'.join).reset_index()

final_all_entity_df['entity_concept']= final_all_entity_df['entity_concept'] + ' ' +'homo sapiens'

final_all_entity_df['ID']=final_all_entity_df.index

final_all_entity_df= final_all_entity_df[['ID','entity','entity_concept','entity_type_id','entity_type']]

final_all_entity_df.to_csv("/home/saikat/diabetes/final_T2DM_all_entity_file.csv",sep=',',index=False)


node_concept= final_all_entity_df['entity_concept'].tolist()

with open("/home/saikat/diabetes/T2DM_entity_concepts.txt",'w') as out:
    for element in node_concept:
        out.write("%s\n"%element)
    




    


     
     
    