#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 16:10:58 2022

@author: saikat
"""

edge_types = []

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

for i in range(len(edge_pair_types)):
    edge_types.append((edge_pair_types[i][0],edge_pair_types[i][0]+'-'+
                       edge_pair_types[i][1],edge_pair_types[i][1]))
    
