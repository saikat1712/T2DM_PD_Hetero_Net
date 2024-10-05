# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 14:17:00 2021

@author: ASUS
"""

snp_snap_tool=[]

############# read file from snpSNAP tool (MIT) matching ###############################

with open(r"D:\SNP_GWAS_dataset\SNPsnap_test_run\input_snps_identifer_mapping.txt") as f, open(r"D:\Epigenomic_proj\snp_snap_diabetes_snps.txt",'w') as out:
        for line in f:
            ind=line.strip('\n').split('\t')
            if ind[0].startswith('snpID')==False:
                snp_snap_tool.append(ind[1])
                out.write("%s\n"%ind[1])
            else:
                pass
                
        
