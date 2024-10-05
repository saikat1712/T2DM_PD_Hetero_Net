#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 16:59:38 2022

@author: saikat
"""

import yaml
from os import listdir
import re
from collections import OrderedDict


# with open("meta.yaml",'r') as f:
#     file = yaml.safe_load(f)
    
# print(file)

### Edge types ####

edge_type_ids = []
edge_files = []
for fname in listdir('/home/saikat/OpenHGNN_test/My_Hetero_net_data_T2DM_dummy/T2DM_hetero_edges'):
    # f_name = re.findall('([edges_*][^.*]+)',fname)
    edge_files.append(fname)
    y=re.findall('([0-9]+)',fname)
    edge_type_ids.append(int(y[0]))

edge_files.sort()
edge_type_ids.sort()

edge_type_dict={}

edge_types= [['pathway','interacts','pathway'],['gene','interacts','gene'],['gene','interacts','downregulated_gene'],
            ['downregulated_gene','rev_interacts','gene'],['gene','interacts','upregulated_gene'],['upregulated_gene','rev_interacts','gene'],
            ['gene','interacts','hypo_methylated_gene'],['hypo_methylated_gene','rev_interacts','gene'],['gene','interacts','hyper_methylated_gene'],['hyper_methylated_gene','rev_interacts','gene'],
            ['gene','interacts','upregulated_hypo_methylated_gene'],['upregulated_hypo_methylated_gene','rev_interacts','gene'],
            ['gene','interacts','downregulated_hypo_methylated_gene'],['downregulated_hypo_methylated_gene','rev_interacts','gene'],
            ['gene','interacts','upregulated_hyper_methylated_gene'],['upregulated_hyper_methylated_gene','rev_interacts','gene'],
            ['gene','interacts','downregulated_hyper_methylated_gene'],['downregulated_hyper_methylated_gene','rev_interacts','gene'],
            ['hypo_methylated_gene','interacts','hypo_methylated_gene'],['hypo_methylated_gene','interacts','upregulated_hypo_methylated_gene'],['upregulated_hypo_methylated_gene','rev_interacts','hypo_methylated_gene'],['hypo_methylated_gene','interacts','downregulated_hypo_methylated_gene'],['downregulated_hypo_methylated_gene','rev_interacts','hypo_methylated_gene'],
            ['upregulated_hypo_methylated_gene','interacts','downregulated_hypo_methylated_gene'],['downregulated_hypo_methylated_gene','rev_interacts','upregulated_hypo_methylated_gene'],['hypo_methylated_gene','interacts','downregulated_gene'],['downregulated_gene','rev_interacts','hypo_methylated_gene'],
            ['downregulated_gene','interacts','upregulated_hypo_methylated_gene'],['upregulated_hypo_methylated_gene','rev_interacts','downregulated_gene'],['upregulated_hypo_methylated_gene','interacts','upregulated_hypo_methylated_gene'],['downregulated_hypo_methylated_gene','interacts','downregulated_hypo_methylated_gene'],
            ['pathway','interacts','gene'],['gene','rev_interacts','pathway'],
            ['pathway','interacts','downregulated_gene'],['downregulated_gene','rev_interacts','pathway'],['pathway','interacts','upregulated_gene'],
            ['upregulated_gene','rev_interacts','pathway'],['pathway','interacts','hypo_methylated_gene'],['hypo_methylated_gene','rev_interacts','pathway'],
            ['pathway','interacts','hyper_methylated_gene'],['hyper_methylated_gene','rev_interacts','pathway'],
            ['pathway','interacts','downregulated_hypo_methylated_gene'],['downregulated_hypo_methylated_gene','rev_interacts','pathway'],['pathway','interacts','upregulated_hypo_methylated_gene'],
            ['upregulated_hypo_methylated_gene','rev_interacts','pathway'],['pathway','interacts','downregulated_hyper_methylated_gene'],['downregulated_hyper_methylated_gene','rev_interacts','pathway'],['pathway','interacts','upregulated_hyper_methylated_gene'],['upregulated_hyper_methylated_gene','rev_interacts','pathway'],['downregulated_gene','interacts','downregulated_gene'],
            ['upregulated_gene','interacts','upregulated_gene'],['rsid_snp','interacts','rsid_snp'],['rsid_snp','interacts','hypo_methylated_gene'],['hypo_methylated_gene','rev_interacts','rsid_snp'],
            ['rsid_snp','interacts','hyper_methylated_gene'],['hyper_methylated_gene','rev_interacts','rsid_snp'],['rsid_snp','interacts','downregulated_hypo_methylated_gene'],['downregulated_hypo_methylated_gene','rev_interacts','rsid_snp'],
            ['rsid_snp','interacts','upregulated_hypo_methylated_gene'],['upregulated_hypo_methylated_gene','rev_interacts','rsid_snp'],['rsid_snp','interacts','downregulated_hyper_methylated_gene'],['downregulated_hyper_methylated_gene','rev_interacts','rsid_snp'],['rsid_snp','interacts','upregulated_hyper_methylated_gene'],
            ['upregulated_hyper_methylated_gene','rev_interacts','rsid_snp'],['rsid_snp','interacts','ptm'],['ptm','rev_interacts','rsid_snp'],['amyloid_protein','interacts','amyloid_protein'],
            ['ptm','interacts','ptm'],['ptm','interacts','amyloid_protein'],['amyloid_protein','rev_interacts','ptm'],['pathway','interacts','icd_t2dm'],['icd_t2dm','rev_interacts','pathway'],
            ['central_amyloid_protein','interacts','central_amyloid_protein'],['central_amyloid_protein','interacts','amyloid_protein'],['amyloid_protein','rev_interacts','central_amyloid_protein'],['ptm','interacts','central_amyloid_protein'],['central_amyloid_protein','rev_interacts','ptm'],
            ['central_amyloid_protein','interacts','icd_t2dm'],['icd_t2dm','rev_interacts','central_amyloid_protein'],['rsid_snp','interacts','icd_t2dm'],['icd_t2dm','rev_interacts','rsid_snp']]



for i in range(len(edge_types)):
    edge_type_dict[i]=edge_types[i]
    
    
T2DM_edge_types={}

for item in edge_type_ids:
    T2DM_edge_types[item] = edge_type_dict[item]
    
edge_data = [{} for i in range(len(edge_files))] ## list of dictionaries of different edge files

for j in range(len(edge_type_ids)):
    for f1 in edge_files:
        y=re.findall('([0-9]+)',f1)
        if int(y[0]) == edge_type_ids[j]:
            edge_data[j]['file_name'] = f1 
            edge_data[j]['etype'] = T2DM_edge_types[edge_type_ids[j]]
            edge_data[j]['src_id_field'] = 'entity1'
            edge_data[j]['dst_id_field'] = 'entity2'
        else:
            pass
        
# with open("test.txt",'w') as f:
#     for v in edge_data:
#         f.write("%s\n"%v)

####################################################################
##### Node types #####        

node_type_ids = []
node_files = []
for fname in listdir('/home/saikat/OpenHGNN_test/My_Hetero_net_data_T2DM_dummy/T2DM_hetero_nodes'):
    # f_name = re.findall('([edges_*][^.*]+)',fname)
    node_files.append(fname)
    y=re.findall('([0-9]+)',fname)
    node_type_ids.append(int(y[0]))

node_files.sort()
node_type_ids.sort()

node_type_dict={}

node_types = ['pathway','downregulated_gene','upregulated_gene','hypo_methylated_gene',
              'hyper_methylated_gene','downregulated_hyper_methylated_gene',
              'upregulated_hyper_methylated_gene','downregulated_hypo_methylated_gene','upregulated_hypo_methylated_gene',
              'gene','rsid_snp','amyloid_protein','central_amyloid_protein',
              'ptm','icd_t2dm']

i=0
for k in node_types:
    node_type_dict[k]=i
    i+=1   

for i in range(len(node_types)):
   node_type_dict[i]=node_types[i]
    
    
T2DM_node_types={}

for item in node_type_ids:
    T2DM_node_types[item] = node_type_dict[item]
    
node_data = [{} for i in range(len(node_files))] ## list of dictionaries of different edge files

for j in range(len(node_type_ids)):
    for f1 in node_files:
        y=re.findall('([0-9]+)',f1)
        if int(y[0]) == node_type_ids[j]:
            node_data[j]['file_name'] = f1 
            node_data[j]['ntype'] = T2DM_node_types[node_type_ids[j]]
            node_data[j]['node_id_field'] = 'entity'
        else:
            pass  

# with open("test1.txt",'w') as f:
#     for v in node_data:
#         f.write("%s\n"%v)
        
#####################################################################

### Making the final dictionary ####

dict_keys = ['version','dataset_name','separator','edge_data','node_data']
dict_values = ['1.0.0', 'T2DM_hetero_data', ',', edge_data, node_data] 

# hetero_dict = {dict_keys[i]: dict_values[i] for i in range(len(dict_keys))}  
hetero_dict = OrderedDict(zip(dict_keys,dict_values))

with open('/home/saikat/OpenHGNN_test/My_Hetero_net_data_T2DM_dummy/meta.yaml','w') as f:
    hetero_meta = yaml.dump(hetero_dict, f, default_flow_style=False, sort_keys=False)
