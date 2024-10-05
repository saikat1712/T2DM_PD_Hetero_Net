# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 12:06:08 2021

@author: ASUS
"""

snp_rsid=[]

with open(r'D:\SNP_GWAS_dataset\SNPsnap_test_run\input_snps_identifer_mapping.txt') as f:
    for line in f:
        if line.startswith('snp')==False:
            ind=line.strip('\n').split('\t')
            snp_rsid.append((ind[0],ind[1]))
        else:
            pass
            

snp_proxy_dict={} 
snp_match=[]           
with open(r'D:\SNP_GWAS_dataset\SNPsnap_test_run\matched_snps.txt') as f:
    for line in f:
        if line.startswith('Input_SNP') == False:
            ind=line.strip('\n').split('\t')
            for i in range(1,10000):
                if ind[0] in snp_proxy_dict:
                    snp_proxy_dict[ind[0]].append(ind[i])
                else:
                    snp_proxy_dict[ind[0]]=[ind[i]]
            
            
            
# print(snp_proxy_dict)  

# snp_proxy_rsid={}

# for k in snp_proxy_dict.keys():
#     for x1,x2 in snp_rsid:
#         if k==x1:           
#            for i in range(len(snp_proxy_dict[k])):               
#                 for x1,x2 in snp_rsid:
#                     if snp_proxy_dict[k][i]==x1:
#                        snp_proxy_dict[k][i]=x2 
#                        k=x2
#                        if snp_proxy_dict[k][i] in snp_proxy_rsid:
#                            snp_proxy_rsid[k].append(snp_proxy_dict[k][i])
#                        else:
#                            snp_proxy_rsid[k]=[snp_proxy_dict[k][i]]
#                     else:
#                         pass
#         else:
#             pass

snp_match=[]
snp_in=[]
snp_ot=[]

for k,v in snp_proxy_dict.items():
    for i in range(len(v)):
        snp_match.append((k,v[i]))
        snp_in.append(k)
        snp_ot.append(v[i])
 
t1=[]         
for x1 in snp_in:
    for a,b in snp_rsid:
        if x1==a:
            t1.append(b)
        else:
            pass
        
t2=[]
for x2 in snp_ot:
    for a,b in snp_rsid:
        if x2==a:
            t2.append(b)
            
final_snp_proxy_rsid=[]

with open(r'D:\SNP_GWAS_dataset\snp_proxy_match_rsid.txt','w') as out:
    for v1,v2 in zip(t1,t2):
        out.write("%s\t%s\n"%(v1,v2))
        final_snp_proxy_rsid.append((v1,v2))
            
            

    