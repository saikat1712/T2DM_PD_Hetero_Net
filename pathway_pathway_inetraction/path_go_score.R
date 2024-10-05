library(reticulate)
use_python('C:\\Users\\SAIKAT\\AppData\\Local\\Programs\\Python\\Python37-32')
library(GOSemSim)
setwd("E:\\workflow_R\\wgcna_blue_mod_pathway\\")
pathway_data=read.csv("path_gene_new.csv",header = T)
df<-data.frame(pathway_data,stringsAsFactors = F)
df$pathway_name <- factor(df$pathway_name, levels=unique(df$pathway_name))
path_list<-list(df$pathway_name)
len_path<-lengths(path_list)
hsGO2 <- godata('org.Hs.eg.db', keytype = "SYMBOL", ont="MF", computeIC=FALSE)


for (i in 1:len_path) {
  gs1<-unname(df[path_list[[1]][i],][[2]])
  s1<-path_list[[1]][i]
  s1<-as.character(s1)
  gs1<-as.character(gs1)
  gs1<-strsplit(gs1,'\"')
  l1<-lengths(gs1)
  g1<-c()
  k1=2
  while (k1<=l1) {
   g1<-c(g1,gs1[[1]][k1])
   k1=k1+2
   
  }

  for (j in 1:len_path) {
    gs2<-unname(df[path_list[[1]][j],][[2]])
    s2<-path_list[[1]][j]
    s2<-as.character(s2)
    gs2<-as.character(gs2)
    gs2<-strsplit(gs2,'\"')
    l2<-lengths(gs2)
    g2<-c()
    k2=2
    while (k2<=l2) {
      g2<-c(g2,gs2[[1]][k2])
      k2=k2+2
    }
    #print(g1)
    #print(g2)
    #print(s1)
    #print(s2)
    score_path<-clusterSim(g1,g2,semData =hsGO2,measure = "Wang",combine = "BMA" )
    source_python("E:\\workflow_R\\wgcna_blue_mod_pathway\\new.py")
    store_val(s1,s2,score_path)
    #all_val<-c(s1,s2,score_path)
    #write.table(all_val,file = "path_path_score.txt",sep="\t",append = T)
    print(score_path)
    
  }
  
  
}
  