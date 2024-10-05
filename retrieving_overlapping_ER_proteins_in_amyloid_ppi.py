#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 17:27:11 2020

@author: saikat
"""

#with open("/home/saikat/Downloads/Epigenomic_proj/ER_poteins_pased.txt",'w') as out:


ppi=[]    
    
with open("/home/saikat/Downloads/Epigenomic_proj/Amyloid_ppi.txt") as f:
    for line in f:
        ind=line.strip('\n').split('\t')
        ppi.append((ind[0],ind[1]))
        
Er_prots=[]

with open("/home/saikat/Downloads/Epigenomic_proj/ER_poteins_pased.txt") as f:
    for line in f:
        ind=line.strip('\n').split('\t')
        Er_prots.append((ind[0],ind[1]))
        

seen=set()        
with open("/home/saikat/Downloads/Epigenomic_proj/overlapping_er_prots.txt",'w') as out:
    for k1,k2 in Er_prots:
        for a1,a2 in ppi:
            if k1==a1 or k1==a2 :
                if k1 not in seen:
                    seen.add(k1)
                    out.write("%s\n"%k1)
            else:
                pass
            
########################## Er overlapps with molecular function #############################

seen=set()        
with open("/home/saikat/Downloads/Epigenomic_proj/overlapping_er_prots_with_MF.txt",'w') as out:
    for k1,k2 in Er_prots:
        for a1,a2 in ppi:
            if k1==a1 or k1==a2 :
                if (k1,k2) not in seen:
                    seen.add((k1,k2))
                    out.write("%s\t%s\n"%(k1,k2))
            else:
                pass
