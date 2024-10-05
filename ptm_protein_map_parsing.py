# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 07:49:46 2020

@author: ASUS
"""

#################### BioGrid PTM data parsing and mapping to PTM ##############################

biogrid_ptm=[]

seen=set()

with open(r'D:\PTM_DATABASE\BIOGRID-PTMS-4.0.189.ptm\BIOGRID-PTM-4.0.189.ptmtab.txt') as f:
    for line in f:
        if line.startswith('#') == False:
            ind=line.strip('\n').split('\t')
            if ind[13]=='9606' :
                biogrid_ptm.append((ind[1],ind[9]))
            else:
                pass

            
with open(r'D:\PTM_DATABASE\PTM_parsed_files\biogrid_ptm_parsed.txt','w') as out:
    for a,b in biogrid_ptm:
        if (a,b) not in seen:
            seen.add((a,b))
            out.write("%s\t%s\n"%(a,b))
        else:
            pass
        
        
##################### Uniprotkb data parsing and mapping to PTM #######################################
        
uniprot_ptm=[]
prot_cleavage=[]

with open(r'D:\PTM_DATABASE\uniprot-filtered-organism__Homo+sapiens+(Human)+[9606]_+AND+review--.tab\uniprot-filtered-organism__Homo+sapiens+(Human)+[9606]_+AND+review--.tab') as f:
    for line in f:
        if line.startswith('Entry') == False:
            ind1=line.strip('\n').split('\t')
            if ind1[2] != '' :
                ind1[2]=ind1[2].lower()
                uniprot_ptm.append((ind1[1],ind1[2]))
                # if 'proteolytic cleavage' and 'proteolytically cleaved' in ind1[2]:
                #     prot_cleavage.append((ind1[1],ind1[2]))
                    
            else:
                pass
        else:
            pass
            
with open(r'D:\PTM_DATABASE\PTM_parsed_files\uniprot_ptm_parsed.txt','w') as out:
    for a,b in uniprot_ptm:
        out.write("%s\t%s\n"%(a,b))   

########## Taking only the proteolytic cleveage PTMs #######################
        
# with open(r'D:\PTM_DATABASE\PTM_parsed_files\ptm_proteolytic_cleveage_parsed.txt','w') as out:
#     for a,b in prot_cleavage:
#         out.write("%s\t%s\n"%(a,b))     
        
################### uniprot_ptm_parsed.txt parsing using Tokenization #################
        
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
stop_wrds=set(stopwords.words('english'))

PTMs= ['proteolytic','cleavage','cleaved','disulfide','bond','carboxylation','oxidation','oxidized','overoxidation ',
     'autoxidation','nitric' ]

# No_carboxylation=['gla','polyglutamate','chains','glycin']

prtr=SnowballStemmer("english")
stem_ptm=[prtr.stem(w) for w in PTMs]

ptm_dict={}

for i in range(len(uniprot_ptm)):
    tokenizer= nltk.RegexpTokenizer(r"\w+")
    new=tokenizer.tokenize(uniprot_ptm[i][1])
    words=[w for w in new if not w in stop_wrds]
    prtr=SnowballStemmer("english")
    stemmed=[prtr.stem(w) for w in words]
    ptm_dict[uniprot_ptm[i][0]]=stemmed

################ ptm dictioanary without stemming #############################
    
ptm_dict_without_stem={}

for i in range(len(uniprot_ptm)):
    tokenizer= nltk.RegexpTokenizer(r"\w+")
    new=tokenizer.tokenize(uniprot_ptm[i][1])
    words=[w for w in new if not w in stop_wrds]
    ptm_dict_without_stem[uniprot_ptm[i][0]]=words


################### proteolytic_cleavage #####################################


proteolyt_prot1=[]
proteolyt_prot2=[]
for k in ptm_dict.keys():
    if  stem_ptm[0]  in ptm_dict[k] and stem_ptm[1] in ptm_dict[k]:
        proteolyt_prot1.append((k,stem_ptm[0]))
    elif  stem_ptm[0] in ptm_dict[k] and stem_ptm[2] in ptm_dict[k]:
        proteolyt_prot2.append((k,stem_ptm[0]))
    else:
        pass

proteolyt= proteolyt_prot1 + proteolyt_prot2
         
with open(r'D:\PTM_DATABASE\PTM_parsed_files\ptm_proteolytic_cleveage_parsed.txt','w') as out:
    for a , b in proteolyt:
        out.write("%s\t%s\n"%(a,b))

###################### disulfide bond #######################################
        
disulfide_prot=[]

with open(r'D:\PTM_DATABASE\PTM_parsed_files\ptm_disulfide_bond_parsed.txt','w') as out:
    for k in ptm_dict.keys():
        if  stem_ptm[3]  in ptm_dict[k] and stem_ptm[4] in ptm_dict[k]:
            disulfide_prot.append((k,stem_ptm[3]))
            out.write("%s\t%s\n"%(k,stem_ptm[3]))
        else:
            pass

##################### carboxylation #########################################

carboxylation_prot=[]

with open(r'D:\PTM_DATABASE\PTM_parsed_files\ptm_caboxylation_parsed.txt','w') as out:
    for k in ptm_dict_without_stem.keys():
        if  PTMs[5]  in ptm_dict_without_stem[k] :
            carboxylation_prot.append((k,PTMs[5]))
            out.write("%s\t%s\n"%(k,PTMs[5]))
        else:
            pass            

#################### oxidation ################################################
            
oxidation_prot=[]

with open(r'D:\PTM_DATABASE\PTM_parsed_files\ptm_oxidation_parsed.txt','w') as out:
    for k in ptm_dict.keys():
        if stem_ptm[6] in ptm_dict[k] or stem_ptm[7] in ptm_dict[k] or stem_ptm[8] in ptm_dict[k] or stem_ptm[9] in ptm_dict[k] :
            if stem_ptm[10] in ptm_dict[k] and abs(ptm_dict[k].index('nitric') - ptm_dict[k].index('oxid')) !=1 :
                oxidation_prot.append((k,stem_ptm[6]))
                out.write("%s\t%s\n"%(k,stem_ptm[6]))
            elif stem_ptm[10] not in ptm_dict[k]:
                out.write("%s\t%s\n"%(k,stem_ptm[6]))
            else:
                pass
        else:
            pass
        
print('completed')