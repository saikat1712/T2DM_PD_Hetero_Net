#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 15:18:57 2020

@author: saikat
"""
import re
cluster_prots=[]

with open(r"D:\Epigenomic_codes\markov_clusters_on_IntAct\neighborhood_amyloid.txt") as f:
    for line in f:
        if line.startswith(' ')==False:
            ind=line.strip('\n').split('\t')
            cluster_prots.append(ind[0])
        else:
            pass


################ keeping ppis if the prot present in the interaction #################

ppi=[]
with open(r'D:\Epigenomic_proj\_all_IntAct_entrez_ppi.txt') as f:
    for line in f:
        ind=line.strip('\n').split('\t')
        ppi.append((ind[0],ind[1]))
        
final_ppi=[]
seen=set()
with open(r'D:\Epigenomic_proj\Amyloid_ppi.txt','w') as out:
    for k in cluster_prots:
        for a,b in ppi:
            if k==a or k==b and (a,b) not in seen:
                seen.add((a,b))
                final_ppi.append((a,b))
                if a!='' and b!='':
                    y1=re.findall('([^ ;]+)',a)
                    y2=re.findall('([^ ;]+)',b)
                    if len(y1)>1 :
                        # for i in range(len(y1)):
                            out.write("%s\t%s\n"%(y1[0],b))
                    elif len(y2)>1:
                        # for j in range(len(y2)):
                            out.write("%s\t%s\n"%(a,y2[0]))
                    else:
                        out.write("%s\t%s\n"%(a,b))
                else:
                    pass
            else:
                pass
            
################### Making network from ER proteins #########################

# ER_prots=[]
# with open("/home/saikat/Downloads/Epigenomic_proj/subcell_location_Endoplasmic.tsv") as f:
#     for line in f:
#         if line.startswith('Gene')==False:
#             ind=line.strip('\n').split('\t')
#             ER_prots.append((ind[0],ind[1],ind[9]))
        
# with open("/home/saikat/Downloads/Epigenomic_proj/ER_poteins.txt",'w') as out:
#     for k1,k2,k3 in ER_prots:
#         out.write("%s\t%s\t%s\n"%(k1,k2,k3))

# temp=[]        
# with open("/home/saikat/Downloads/Epigenomic_proj/temp_er_prots.txt",'w') as out:
#     for a,b,c in ER_prots:
#         temp.append((a,c))
#         out.write("%s\t%s\n"%(a,c))
#         if b!='':
#             y=re.findall('([^ ",]+)',b)
#             for i in range(len(y)):
#                 temp.append((y[i],c))
#                 out.write("%s\t%s\n"%(y[i],c))
                
# uni_gene=[]
# with open("/home/saikat/Downloads/Epigenomic_proj/uniprot-filtered-organism__Homo+sapiens+(Human)+[9606]_+AND+review--.tab") as f:
#     for line in f:
#         if line.startswith('Entry')==False:
#             ind=line.strip('\n').split('\t')
#             uni_gene.append(ind[1])
            
# with open("/home/saikat/Downloads/Epigenomic_proj/ER_poteins_pased.txt",'w') as out:
#     for k1,k2 in temp:
#         for g in uni_gene:
#             if k1==g:
#                 out.write("%s\t%s\n"%(k1,k2))
#             else:
#                 pass
            
            
            
print("completed")
        