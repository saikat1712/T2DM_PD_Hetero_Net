#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 20:59:46 2020

@author: saikat
"""

import re
temp=[]
with open("/home/saikat/Downloads/Epigenomic_proj/IntAct_protein_datatsets/intact.txt") as f:
    for line in f:
        if line.startswith('#')==False:
            ind=line.strip('\n').split('\t')
            if ind[28].startswith('taxid:9606')==True and ind[0].startswith('uniprotkb:')==True:
                y1=re.findall('([^ uniprotkb:]+)',ind[0])
                y2=y=re.findall('([^ uniprotkb:]+)',ind[1])
                temp.append((y1[0],y2[0],ind[28]))
            else:
                pass

seen=set() 
l1=[]
l2=[]           
with open("/home/saikat/Downloads/Epigenomic_proj/parsed_ppi.txt",'w') as out:
    for k1,k2,k3 in temp:
        if (k1,k2) not in seen:
            seen.add((k1,k2))
            l1.append(k1)
            l2.append(k2)
            out.write("%s\t%s\n"%(k1,k2))
        else:
            pass

prot_gene=[]        
with open("/home/saikat/Downloads/Epigenomic_proj/uniprot-filtered-organism__Homo+sapiens+(Human)+[9606]_+AND+review--.tab") as f:
    for line in f:
        if line.startswith('Entry')==False:
            ind=line.strip('\n').split('\t')
            prot_gene.append((ind[0],ind[1]))
g1=[] 
g2=[]           
for x in l1:
    for a,b in prot_gene:
        if x==a:
            g1.append(b)
        else:
            pass
        
for x1 in l2:
    for a,b in prot_gene:
        if x1==a:
            g2.append(b)
            
        else:
            pass
        
with open("/home/saikat/Downloads/Epigenomic_proj/final_entrez_ppi.txt",'w') as out:
    for v1,v2 in zip(g1,g2):
        out.write("%s\t%s\n"%(v1,v2))
        
print("Completed")
            
