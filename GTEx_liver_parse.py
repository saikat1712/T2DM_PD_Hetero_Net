#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 20:18:09 2021

@author: saikat
"""

import re

liver_gtx=[]

with open("/home/saikat/Datasets/Liver.v8.egenes.txt") as f:
    for line in f:
        if line.startswith('gene_id')==False:
            ind=line.strip('\n').split('\t')
            y1=re.findall('([^ .]+)',ind[0])
            y2=re.findall('([^ chr]+)',ind[13])
            liver_gtx.append((y1[0],y2[0],ind[15],ind[16],ind[18],ind[21]))
        else:
            pass
        
# print(liver_gtx)

#################### mapping to the ensembl-vep rsid od diabetes ######################################
        