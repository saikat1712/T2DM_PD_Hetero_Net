#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 23:32:40 2020

@author: saikat
"""

import re
p1=[]
with open("/home/saikat/Downloads/Epigenomic_proj/IntAct_protein_datatsets/P0DJI9.txt") as f:
    for line in f:
        if line.startswith('#')==False:
            ind=line.strip('\n').split('\t')
            if ind[0].startswith('uniprotkb:') and ind[1].startswith('uniprotkb:')==True:
                y1=re.findall('([^ uniprotkb:]+)',ind[0])
                y2=y=re.findall('([^ uniprotkb:]+)',ind[1])
                p1.append((y1[0],y2[0]))
            
p2=[]      
with open("/home/saikat/Downloads/Epigenomic_proj/IntAct_protein_datatsets/P10997.txt") as f:
    for line in f:
        if line.startswith('#')==False:
            ind=line.strip('\n').split('\t')
            if ind[0].startswith('uniprotkb:') and ind[1].startswith('uniprotkb:')==True:
                y1=re.findall('([^ uniprotkb:]+)',ind[0])
                y2=y=re.findall('([^ uniprotkb:]+)',ind[1])
                p2.append((y1[0],y2[0]))
                
p=list(set(p1+p2))

print(p)

l1=[]
l2=[]
with open("/home/saikat/Downloads/Epigenomic_proj/P0DJI9_P10997.txt",'w') as out:
    for k1,k2 in p:
        l1.append(k1)
        l2.append(k2)
        out.write("%s\t%s\n"%(k1,k2))
        
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
        
with open("/home/saikat/Downloads/Epigenomic_proj/P0DJI9_P10997_entrez_ppi.txt",'w') as out:
    for v1,v2 in zip(g1,g2):
        out.write("%s\t%s\n"%(v1,v2))
        
filenames=['/home/saikat/Downloads/Epigenomic_proj/final_entrez_ppi.txt','/home/saikat/Downloads/Epigenomic_proj/P0DJI9_P10997_entrez_ppi.txt']

with open("/home/saikat/Downloads/Epigenomic_proj/_all_IntAct_entrez_ppi.txt",'w') as out:
    for fname in filenames:
        with open(fname) as f:
            for line in f:
                out.write(line)

        
print("Completed")