#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 21:27:10 2021

@author: saikat
"""

import pandas as pd

from os import listdir

## entity-entity_type dictionary ##


entities_df = pd.read_csv("/home/saikat/diabetes/final_T2DM_all_entity_file.csv")

entities_df = entities_df.drop(columns=['ID','entity_concept','entity_type_id'])

entities_df.set_index('entity', inplace=True)

entity_type_dict = entities_df.to_dict()['entity_type']

    
edge_pair_types= [['pathway','pathway'],['gene','gene'],['gene','downregulated_gene'],
            ['downregulated_gene','gene'],['gene','upregulated_gene'],['upregulated_gene','gene'],
            ['gene','hypo_methylated_gene'],['hypo_methylated_gene','gene'],['gene','hyper_methylated_gene'],['hyper_methylated_gene','gene'],
            ['gene','upregulated_hypo_methylated_gene'],['upregulated_hypo_methylated_gene','gene'],
            ['gene','downregulated_hypo_methylated_gene'],['downregulated_hypo_methylated_gene','gene'],
            ['gene','upregulated_hyper_methylated_gene'],['upregulated_hyper_methylated_gene','gene'],
            ['gene','downregulated_hyper_methylated_gene'],['downregulated_hyper_methylated_gene','gene'],
            ['hypo_methylated_gene','hypo_methylated_gene'],['hypo_methylated_gene','upregulated_hypo_methylated_gene'],['upregulated_hypo_methylated_gene','hypo_methylated_gene'],['hypo_methylated_gene','downregulated_hypo_methylated_gene'],['downregulated_hypo_methylated_gene','hypo_methylated_gene'],
            ['upregulated_hypo_methylated_gene','downregulated_hypo_methylated_gene'],['downregulated_hypo_methylated_gene','upregulated_hypo_methylated_gene'],['hypo_methylated_gene','downregulated_gene'],['downregulated_gene','hypo_methylated_gene'],
            ['downregulated_gene','upregulated_hypo_methylated_gene'],['upregulated_hypo_methylated_gene','downregulated_gene'],['upregulated_hypo_methylated_gene','upregulated_hypo_methylated_gene'],['downregulated_hypo_methylated_gene','downregulated_hypo_methylated_gene'],
            ['pathway','gene'],['gene','pathway'],
            ['pathway','downregulated_gene'],['downregulated_gene','pathway'],['pathway','upregulated_gene'],
            ['upregulated_gene','pathway'],['pathway','hypo_methylated_gene'],['hypo_methylated_gene','pathway'],['pathway','hyper_methylated_gene'],['hyper_methylated_gene','pathway'],
            ['pathway','downregulated_hypo_methylated_gene'],['downregulated_hypo_methylated_gene','pathway'],['pathway','upregulated_hypo_methylated_gene'],
            ['upregulated_hypo_methylated_gene','pathway'],['pathway','downregulated_hyper_methylated_gene'],['downregulated_hyper_methylated_gene','pathway'],['pathway','upregulated_hyper_methylated_gene'],['upregulated_hyper_methylated_gene','pathway'],['downregulated_gene','downregulated_gene'],
            ['upregulated_gene','upregulated_gene'],['rsid_snp','rsid_snp'],['rsid_snp','hypo_methylated_gene'],['hypo_methylated_gene','rsid_snp'],
            ['rsid_snp','hyper_methylated_gene'],['hyper_methylated_gene','rsid_snp'],['rsid_snp','downregulated_hypo_methylated_gene'],['downregulated_hypo_methylated_gene','rsid_snp'],
            ['rsid_snp','upregulated_hypo_methylated_gene'],['upregulated_hypo_methylated_gene','rsid_snp'],['rsid_snp','downregulated_hyper_methylated_gene'],['downregulated_hyper_methylated_gene','rsid_snp'],['rsid_snp','upregulated_hyper_methylated_gene'],
            ['upregulated_hyper_methylated_gene','rsid_snp'],['rsid_snp','ptm'],['ptm','rsid_snp'],['amyloid_protein','amyloid_protein'],
            ['ptm','ptm'],['ptm','amyloid_protein'],['amyloid_protein','ptm'],['pathway','central_amyloid_protein_t2dm_E11.8'],['central_amyloid_protein_t2dm_E11.8','pathway'],
            ['central_amyloid_protein_t2dm_E11.8','central_amyloid_protein_t2dm_E11.8'],['central_amyloid_protein_t2dm_E11.8','amyloid_protein'],['amyloid_protein','central_amyloid_protein_t2dm_E11.8'],['ptm','central_amyloid_protein_t2dm_E11.8'],['central_amyloid_protein_t2dm_E11.8','ptm'],
            ['rsid_snp','central_amyloid_protein_t2dm_E11.8'],['central_amyloid_protein_t2dm_E11.8','rsid_snp']]

edge_types = []

for i in range(len(edge_pair_types)):
    edge_types.append((edge_pair_types[i][0],edge_pair_types[i][0]+'-'+
                       edge_pair_types[i][1],edge_pair_types[i][1]))
    
    
#### edge dictionary ######

edge_type_dict={}


i=0
for k in edge_types:
    edge_type_dict[k]=i
    i+=1

edge_dict = {}


for i in range(len(edge_types)):
    edge_dict[tuple(edge_pair_types[i])] = edge_types[i]


## integration of Pathway-Pathway subnetworks for all modules

path='/home/saikat/diabetes/sem_pheno_modules/'

path_frames=[]
for filename in listdir("/home/saikat/diabetes/sem_pheno_modules"):
    df_path=pd.read_csv(path+filename)
    path_frames.append(df_path)
final_df_path=pd.concat(path_frames,ignore_index=True)
final_df_path=final_df_path.drop(columns=['semantic_score','phenotype_entropy'])
final_df_path=final_df_path.dropna()
final_df_path=final_df_path.rename(columns={'pathway1':'entity1','pathway2':'entity2','Edge_weight':'edge_weight'})



# integration of Gene-Coexpression modules

coexpression_frames=[]
path='/home/saikat/diabetes/gene_coexpression_subnetworks/'
for fname in listdir('/home/saikat/diabetes/gene_coexpression_subnetworks'):
    if fname.startswith('CytoscapeInput_edges_') and fname.endswith('.csv'):
        df_gene=pd.read_csv(path+fname,sep='\t')
        coexpression_frames.append(df_gene)
    else:
        pass   
    
final_df_genecoexpression=pd.concat(coexpression_frames,ignore_index=True)
final_df_genecoexpression=final_df_genecoexpression.drop(columns=['direction','fromAltName','toAltName'])
final_df_genecoexpression=final_df_genecoexpression.dropna()
final_df_genecoexpression=final_df_genecoexpression.rename(columns={'fromNode':'entity1','toNode':'entity2','weight':'edge_weight'})



## integration of SNP-SNP interactions

df_snp=pd.read_csv("/home/saikat/diabetes/plink.epi.cc.txt",sep='\s+')

df_snp= df_snp[['SNP1','SNP2']]
final_df_snp= df_snp.rename(columns={'SNP1':'entity1','SNP2':'entity2'})
final_df_snp['edge_weight'] = -9999


# integration of module specific pathway-gene interacions

path= "/home/saikat/diabetes/genecoexpression_specific_path_gene_associations/"

path_gene_frames=[]
for filename in listdir("/home/saikat/diabetes/genecoexpression_specific_path_gene_associations"):
    df_path_gene=pd.read_csv(path+filename)
    path_gene_frames.append(df_path_gene)
    
final_df_path_gene=pd.concat(path_gene_frames,ignore_index=True)
final_df_path_gene=final_df_path_gene.dropna()
final_df_path_gene=final_df_path_gene.rename(columns={'gene_symbol':'entity1','pathway_name':'entity2'})
final_df_path_gene['edge_weight'] = -9999


final_df_path_gene.to_csv("/home/saikat/diabetes/path_gene_test.csv",index=None)
# integration of module specific pathway to ICD-E11.8 (obtained using page_rank centrality measure on Pathway network)

# path= "/home/saikat/diabetes/pathway_to_ICD_for_each_modules/"

# path_icd_frames=[]
# for filename in listdir("/home/saikat/diabetes/pathway_to_ICD_for_each_modules"):
#     df_path_icd=pd.read_csv(path+filename)
#     path_icd_frames.append(df_path_icd)

# final_df_path_icd=pd.concat(path_icd_frames,ignore_index=True)
# final_df_path_icd=final_df_path_icd.dropna()
# final_df_path_icd=final_df_path_icd.rename(columns={'node':'entity1','ICD':'entity2'}) 
# final_df_path_icd['edge_weight']= -9999  


## integration of Amyloid_PPI_PTM network

final_df_amyloid_ppi_ptm_net=pd.read_csv("/home/saikat/diabetes/central_prot_replaced_newly_named_amy_ppi_net.csv")
final_df_amyloid_ppi_ptm_net=final_df_amyloid_ppi_ptm_net.rename(columns={'node1':'entity1','node2':'entity2'})
final_df_amyloid_ppi_ptm_net['edge_weight']= -9999
final_df_amyloid_ppi_ptm_net=final_df_amyloid_ppi_ptm_net[['entity1','entity2','edge_weight']]


# amynet_ptm=[] 

# with open("/home/saikat/Epigenomic_proj/final_amyloid_ppi_ptm_network.txt") as f:
#     for line in f:
#         ind=line.strip('\n').split('\t')
#         amynet_ptm.append((ind[0],ind[1]))
        
# final_df_amyloid_ppi_ptm_net= pd.DataFrame(amynet_ptm,columns=['entity1','entity2'])
# final_df_amyloid_ppi_ptm_net=final_df_amyloid_ppi_ptm_net.dropna()

## integration of Amyloid central proteins to ICD-E11.8

# final_df_amy_central_icd=pd.read_csv("/home/saikat/Epigenomic_proj/Amyloid_central_id_to_ICD-10_E11.8.csv")
# final_df_amy_central_icd=final_df_amy_central_icd.rename(columns={'Central_protein':'entity1','ICD-10-T2DM':'entity2'})
# final_df_amy_central_icd['edge_weight']= -9999


## integration of SNP-PTM inetraction

snp_ptm=[]

with open("/home/saikat/Heterogeneous_diabetes/T2DM_snp_ptm_final.txt") as f:
    for line in f:
        ind=line.strip('\n').split('\t')
        snp_ptm.append((ind[0],ind[1]))
        
final_df_snp_ptm= pd.DataFrame(snp_ptm, columns=['entity1','entity2'])
final_df_snp_ptm['edge_weight']= -9999


## interation of SNP-DMGs (Differentially Methylated Genes), RSID-DMGs
## As here only hypomethylation overlap exists, so hypermethylation association doesn't exist

final_df_snp_dmg=pd.read_csv("/home/saikat/Heterogeneous_diabetes/diabetes_2_Methylation_overlap/hypo_vep_overlap.csv")

final_df_snp_dmg=final_df_snp_dmg[['RSID','gene_name']]
final_df_snp_dmg=final_df_snp_dmg.dropna()
final_df_snp_dmg=final_df_snp_dmg.rename(columns={'RSID':'entity1','gene_name':'entity2'})
final_df_snp_dmg['edge_weight']= -9999


## integration of SNP-ICD-E11.8 if and only if SNP is associated with Type 2 diabetes Mellitus associated

# final_df_snp_icd= pd.read_csv("/home/saikat/Heterogeneous_diabetes/T2DM_RSIDs_to_ICD_only.csv")
# final_df_snp_icd=final_df_snp_icd.rename(columns={'rsID':'entity1','ICD':'entity2'})
# final_df_snp_icd['edge_weight']= -9999

## integration of all pathway_snp_central_protein to ICD-E11.8 connected subnetwork after edge contraction 

final_pathway_central_amy_snp_icd_subnet = pd.read_csv('/home/saikat/diabetes/pathway_icd_snp_central_amy_prot_subgraph_after_edge_contract.csv')
final_pathway_central_amy_snp_icd_subnet = final_pathway_central_amy_snp_icd_subnet.drop_duplicates()
final_pathway_central_amy_snp_icd_subnet = final_pathway_central_amy_snp_icd_subnet.dropna()
final_pathway_central_amy_snp_icd_subnet['edge_weight'] = -9999



all_subnet_frames=[final_df_path,final_df_genecoexpression,final_df_path_gene,final_df_snp,final_df_snp_ptm,final_df_snp_dmg,final_df_amyloid_ppi_ptm_net,final_pathway_central_amy_snp_icd_subnet]

Heterogeneous_Network=pd.concat(all_subnet_frames,ignore_index=True)

Heterogeneous_Network.to_csv("/home/saikat/diabetes/final_heterogeneous_network.csv",sep=',',index=None,header=True)

Heterogeneous_Network_1 = Heterogeneous_Network[['entity2','entity1','edge_weight']]

Heterogeneous_Network_1 = Heterogeneous_Network_1.rename(columns={'entity2':'entity1','entity1':'entity2'})
Hetero_frames = [Heterogeneous_Network, Heterogeneous_Network_1]

Heterogeneous_Network_final = pd.concat(Hetero_frames, ignore_index= True)

Heterogeneous_Network_final = Heterogeneous_Network_final.drop_duplicates()

Heterogeneous_Network_final.to_csv("/home/saikat/diabetes/final_heterogeneous_network_bidirectional.csv",index=None,header=True)


## Make a dictionary from entity id to entity types

Heterogeneous_Network_final = Heterogeneous_Network_final.assign(entity1_type = '',
                                                                entity2_type = '' )

# Using apply() for fast looping through the dataframe 'Heterogeneous_Network_final'

def entity_type_compare(row):
    d=Heterogeneous_Network_final
    a = row.entity1
    b = row.entity2
    if a in entity_type_dict.keys():
        d.at[row.name,'entity1_type'] = entity_type_dict[a]
    if b in entity_type_dict.keys():
        d.at[row.name,'entity2_type'] = entity_type_dict[b] 
    else:
        pass
    
            
# ddata = dd.from_pandas(Heterogeneous_Network_final, npartitions= 10)

df3 = Heterogeneous_Network_final.apply(entity_type_compare, axis=1) # df3 dataframe is updating every time as an instance of Heterogeneous_Network_final

# Heterogeneous_Network_final.to_csv("/home/saikat/my_server_codes_data_T2DM/hetero_net_partial.csv",index=None)
           
###################################  

# Making the combined entity_type in the Heterogeneous Network ###

Heterogeneous_Network_final['combined_entity_type'] = Heterogeneous_Network_final[['entity1_type','entity2_type']].agg(','.join, axis=1)

Heterogeneous_Network_final['combined_entity_type'] = Heterogeneous_Network_final[['entity1_type','entity2_type']].values.tolist()


def get_type_id(row):
    d=Heterogeneous_Network_final
    for key, value in edge_dict.items():
        if row['combined_entity_type'] == list(key):
            d.at[row.name,'entity_pair_type'] = str(key)
            d.at[row.name, 'edge_type_id'] = edge_type_dict[value]
            d.at[row.name, 'edge_type'] = str(value)
        else:
            pass
               
        
df4 = Heterogeneous_Network_final.apply(get_type_id, axis=1)

Heterogeneous_Network_final = Heterogeneous_Network_final[['entity1','entity2','edge_weight','entity1_type',
                                                            'entity2_type','combined_entity_type','entity_pair_type','edge_type','edge_type_id']]

## Finally partially weighted Heterogeneous Network saving in the csv file ##             

Heterogeneous_Network_final.to_csv("/home/saikat/diabetes/final_hetero_bidirectional_network_with_edge_types.csv",index=None)        


        

