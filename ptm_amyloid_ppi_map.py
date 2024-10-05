# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 07:47:27 2020

@author: ASUS
"""


from os import listdir
import pandas as pd

path1='/home/saikat/Datasets/PTM_DATABASE/dbPTM_database/PTMs/'

dbptm=[]
seen=set()
with open('/home/saikat/Epigenomic_proj/dbptm_prots.txt','w') as out:
    for filename in listdir("/home/saikat/Datasets/PTM_DATABASE/dbPTM_database/PTMs"):
            with open(path1 + filename) as currentFile:
                # text=currentFile.read()
                for line in currentFile:
                    ind=line.strip('\n').split('\t')
                    if '_HUMAN' in ind[0] :
                        if (ind[3],ind[1]) not in seen:
                            seen.add((ind[3],ind[1]))
                            dbptm.append((ind[3],ind[1]))
                            out.write("%s\t%s\t%s\n"%(ind[0],ind[3],ind[1]))  
                        else:
                            pass
                    else:
                        pass
                    
# print(dbptm)  
# print(len(dbptm))
                        
######################## protein to gene name mappings #####################################

prot_gene=[]                        

with open('/home/saikat/Epigenomic_proj/uniprot-filtered-organism__Homo+sapiens+(Human)+[9606]_+AND+review/uniprot-filtered-organism__Homo+sapiens+(Human)+[9606]_+AND+review--.tab') as f:
    for line in f:
        ind=line.strip('\n').split('\t')
        if ind[0].startswith('Entry')== False:
            prot_gene.append((ind[0],ind[1],ind[3]))
        else:
            pass


df_uniprot=pd.DataFrame(prot_gene,columns=['Protein','Gene','Synonym'])
df_uniprot['Gene'] = df_uniprot['Gene'].str.split(';')
df_uniprot = df_uniprot.explode('Gene')
df_uniprot['Synonym']= df_uniprot['Synonym'].str.split(' ')
df_uniprot= df_uniprot.explode('Synonym')
df_uniprot= df_uniprot.drop_duplicates()
uniprot_genes=df_uniprot['Gene'].tolist() + df_uniprot['Synonym'].tolist()
uniprot_genes=list(set(uniprot_genes))

### dbPTM proteins to gene mappings
        
dbptm_gene=[]

pair=set()
for a1,a2 in dbptm:
    for x1,x2,x3 in prot_gene:
        if a2==x1 and (a1,x2) not in pair:
            pair.add((a1,x2))
            dbptm_gene.append((a1,x2))
            
with open('/home/saikat/Epigenomic_proj/dbptm_genes.txt','w') as out:
    for k1,k2 in dbptm_gene:
        out.write("%s\t%s\n"%(k1,k2))
                        
path2='/home/saikat/Datasets/PTM_DATABASE/PTM_parsed_files/other_ptms/'

uniprot_ptm=[]

with open('/home/saikat/uniprot_ptm_prots.txt','w') as out:
    for filename in listdir("/home/saikat/Datasets/PTM_DATABASE/PTM_parsed_files/other_ptms"):
            with open(path2 + filename) as currentFile:
                # text=currentFile.read()
                for line in currentFile:
                    ind=line.strip('\n').split('\t')
                    uniprot_ptm.append((ind[1],ind[0]))
                    out.write("%s\t%s\n"%(ind[1],ind[0])) 
                            

all_ptms= dbptm_gene + uniprot_ptm

with open('/home/saikat/Epigenomic_proj/all_ptm_gene_associations.txt','w') as out:
    for a,b in all_ptms:
        out.write("%s\t%s\n"%(a,b))
        
############ creating dictionary of ptm_to_genes ##############
        
ptm_gene_associations={}

for k,v in all_ptms:
    if k in ptm_gene_associations:
        ptm_gene_associations[k].append(v)
    else:
        ptm_gene_associations[k]= [v]
        
        
with open('/home/saikat/Epigenomic_proj/all_ptm_gene_dict.txt','w') as out:
    for k1,v1 in ptm_gene_associations.items():
        out.write("%s\t%s\n"%(k1,v1))
                    
#################### retrieving the proteins of amyloid ppi ##################################

prot1=[]        
prot2=[]
amyloid_interaction=[]
with open('/home/saikat/Epigenomic_proj/Amyloid_ppi.txt') as f:
    for line in f:
        ind=line.strip('\n').split('\t')
        amyloid_interaction.append((ind[0],ind[1]))
        prot1.append(ind[0])
        prot2.append(ind[1])
        
all_prot=list(set(prot1+prot2))

### Intersection from parsed uniprot genes

amyprot_with_unigenes=list(set(all_prot).intersection(set(uniprot_genes)))

## keep the amyloid intersection proteins if it exists in the uniprot, else discard

amy_net_final=[]
seen=set()
for v1,v2 in amyloid_interaction:
    if v1 in amyprot_with_unigenes and v2 in amyprot_with_unigenes:
        if (v1,v2) not in seen:
            seen.add((v1,v2))
            amy_net_final.append((v1,v2))
        else:
            pass            
    else:
        pass
##################################################

ptm_amyloid={}

for x in ptm_gene_associations.keys():
    ptm_amyloid[x]=list(set(ptm_gene_associations[x]) & set(amyprot_with_unigenes))
    
with open('/home/saikat/Epigenomic_proj/all_ptm_amyloid_dict.txt','w') as out:
    for x1,x2 in ptm_amyloid.items():
        out.write("%s\t%s\n"%(x1,x2))

ptm_prots= []  
      
for k11 in ptm_amyloid.keys():
    for val in ptm_amyloid[k11]:
        ptm_prots.append((k11,val))
        
with open('/home/saikat/Epigenomic_proj/ptm_to_amyloid_prots.txt','w') as out:
    for (x11,x22) in ptm_prots:
        out.write("%s\t%s\n"%(x11,x22))

mixed_interaction= amy_net_final + ptm_prots

with open("/home/saikat/Epigenomic_proj/amyloid_with_ptm_prots_associations.txt",'w') as out:
    for n1,n2 in mixed_interaction:
        out.write("%s\t%s\n"%(n1,n2))
        
print("completed")