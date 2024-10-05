#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 19:09:39 2020

@author: saikat
"""
import re
import string

Amy_in_vivo=['P05067','P02647','P02652','P06727','P61769','P01258','Q15517','P01034','P02671','P47929','P06396','P01308','Q9Y287','P10997','Q15582','Q08431',
'P02788','O14960','P61626','P04156','P01160','A1E959','P01236','P11686','P04279','P0DJI8','P0DJI9','P02766']

Amy_in_vitro=['P02511','P37840','P02655','P42574','P13569','P42858','P49768','P49810','Q13813','P10636','P60709','P02649','P54253']

prot_gene=[]
with open(r'D:\Epigenomic_proj\uniprot-filtered-organism__Homo+sapiens+(Human)+[9606]_+AND+review--.tab\uniprot-filtered-organism__Homo+sapiens+(Human)+[9606]_+AND+review--.tab') as f:
    for line in f:
        if line.startswith('Entry')==False:
            ind=line.strip('\n').split('\t')
            prot_gene.append((ind[0],ind[1]))

####################### Mapping the Amyloid Precursors to their gene names ##################### 

Amy_prot = Amy_in_vivo + Amy_in_vitro

amy_prt_map=[]
Amy_prot_gene=[]           
for p in Amy_prot:
    for x1,x2 in prot_gene:
        if p==x1:
            Amy_prot_gene.append(x2)
            amy_prt_map.append((x2,x1))
        else:
            pass
        
print(Amy_prot_gene)

with open(r'D:\Epigenomic_proj\uniprot-filtered-organism__Homo+sapiens+(Human)+[9606]_+AND+review--.tab\uniprot_gene.txt','w') as out:
    for a1,a2 in amy_prt_map:
        out.write("%s\t%s\n"%(a1,a2))

#################### apply searching over multiple clusters  #######################


from os import listdir

dis_files=[]
path='D:\\Epigenomic_codes\\markov_clusters_on_IntAct\\clusters\\'
with open(r'D:\Epigenomic_codes\markov_clusters_on_IntAct\result.txt', 'w') as f:
    for k in Amy_prot_gene:
        for filename in listdir(r"D:\Epigenomic_codes\markov_clusters_on_IntAct\clusters"):
            with open(path + filename) as currentFile:
                text = currentFile.read()
                if k in text:
                    f.write('Amyloid_gene_present_' + filename + '\n')
                    dis_files.append(path+filename)
                else:
                    pass
                
filenames=list(set(dis_files))

# print(filenames)

seen=set()
with open(r"D:\Epigenomic_codes\markov_clusters_on_IntAct\neighborhood_amyloid.txt",'w') as out:
    for filename in filenames:
        with open(filename) as f:
            for line in f:
                if line not in seen:
                    seen.add(line)
                    if ';' in line:
                        y=re.findall('([^ ;]+)',line)
                        for i in range(len(y)):
                            out.write(y[i])
                            out.write('\n')
                    else:
                        out.write(line)
                else:
                    pass
                
                


