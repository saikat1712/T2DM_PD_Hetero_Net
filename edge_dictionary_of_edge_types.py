#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 24 20:11:37 2022

@author: saikat
"""

edge_type_dict={}

edge_types= [['pathway','interacts','pathway'],['gene','interacts','gene'],['gene','interacts','downregulated_gene'],
            ['downregulated_gene','rev_interacts','gene'],['gene','interacts','upregulated_gene'],['upregulated_gene','rev_interacts','gene'],
            ['gene','interacts','hypo_methylated_gene'],['hypo_methylated_gene','rev_interacts','gene'],['gene','interacts','hyper_methylated_gene'],['hyper_methylated_gene','rev_interacts','gene'],
            ['gene','interacts','upregulated_hypo_methylated_gene'],['upregulated_hypo_methylated_gene','rev_interacts','gene'],
            ['gene','interacts','downregulated_hypo_methylated_gene'],['downregulated_hypo_methylated_gene','rev_interacts','gene'],
            ['gene','interacts','upregulated_hyper_methylated_gene'],['upregulated_hyper_methylated_gene','rev_interacts','gene'],
            ['gene','interacts','downregulated_hyper_methylated_gene'],['downregulated_hyper_methylated_gene','rev_interacts','gene'],
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
            ['central_amyloid_protein','interacts','icd_t2dm'],['icd_t2dm','rev_interacts','central_amyloid_protein'],['rsid_snp','interacts','icd_t2dm'],['icd_t2dm','rev_interacts','rsid_snp']]


i=0
for k in edge_types:
    edge_type_dict[tuple(k)]=i
    i+=1
    
edge_pair_types= [['pathway','pathway'],['gene','gene'],['gene','downregulated_gene'],
            ['downregulated_gene','gene'],['gene','upregulated_gene'],['upregulated_gene','gene'],
            ['gene','hypo_methylated_gene'],['hypo_methylated_gene','gene'],['gene','hyper_methylated_gene'],['hyper_methylated_gene','gene'],
            ['gene','upregulated_hypo_methylated_gene'],['upregulated_hypo_methylated_gene','gene'],
            ['gene','downregulated_hypo_methylated_gene'],['downregulated_hypo_methylated_gene','gene'],
            ['gene','upregulated_hyper_methylated_gene'],['upregulated_hyper_methylated_gene','gene'],
            ['gene','downregulated_hyper_methylated_gene'],['downregulated_hyper_methylated_gene','gene'],
            ['pathway','gene'],['gene','pathway'],
            ['pathway','downregulated_gene'],['downregulated_gene','pathway'],['pathway','upregulated_gene'],
            ['upregulated_gene','pathway'],['pathway','hypo_methylated_gene'],['hypo_methylated_gene','pathway'],['pathway','hyper_methylated_gene'],['hyper_methylated_gene','pathway'],
            ['pathway','downregulated_hypo_methylated_gene'],['downregulated_hypo_methylated_gene','pathway'],['pathway','upregulated_hypo_methylated_gene'],
            ['upregulated_hypo_methylated_gene','pathway'],['pathway','downregulated_hyper_methylated_gene'],['downregulated_hyper_methylated_gene','pathway'],['pathway','upregulated_hyper_methylated_gene'],['upregulated_hyper_methylated_gene','pathway'],['downregulated_gene','downregulated_gene'],
            ['upregulated_gene','upregulated_gene'],['rsid_snp','rsid_snp'],['rsid_snp','hypo_methylated_gene'],['hypo_methylated_gene','rsid_snp'],
            ['rsid_snp','hyper_methylated_gene'],['hyper_methylated_gene','rsid_snp'],['rsid_snp','downregulated_hypo_methylated_gene'],['downregulated_hypo_methylated_gene','rsid_snp'],
            ['rsid_snp','upregulated_hypo_methylated_gene'],['upregulated_hypo_methylated_gene','rsid_snp'],['rsid_snp','downregulated_hyper_methylated_gene'],['downregulated_hyper_methylated_gene','rsid_snp'],['rsid_snp','upregulated_hyper_methylated_gene'],
            ['upregulated_hyper_methylated_gene','rsid_snp'],['rsid_snp','ptm'],['ptm','rsid_snp'],['amyloid_protein','amyloid_protein'],
            ['ptm','ptm'],['ptm','amyloid_protein'],['amyloid_protein','ptm'],['pathway','icd_t2dm'],['icd_t2dm','pathway'],
            ['central_amyloid_protein','icd_t2dm'],['icd_t2dm','central_amyloid_protein'],['rsid_snp','icd_t2dm'],['icd_t2dm','rsid_snp']]

edge_dict = {}


for i in range(len(edge_types)):
    edge_dict[tuple(edge_pair_types[i])] = edge_types[i]
    
with open("/home/saikat/Epigenomic_proj/edge_types_dictionary_values.txt",'w') as out:
    for k,v in edge_dict.items():
        out.write("%s\t%s\n"%(k,v))