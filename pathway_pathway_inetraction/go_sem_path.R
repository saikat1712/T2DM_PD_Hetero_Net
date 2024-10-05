library(plyr)
library(dplyr)
library(stringr)
library(GOSemSim)
setwd("E:\\workflow_R\\wgcna_blue_mod_pathway\\")
pathway_data=read.csv("path_gene_new.csv",header = T,nrows = 30)
df<-data.frame(pathway_data)
path_list<-list(df$pathway_name)
len_path<-lengths(path_list)
hsGO2 <- godata('org.Hs.eg.db', keytype = "SYMBOL", ont="MF", computeIC=FALSE)

for (i in 1:len_path) {
  gs1<-unname(df[path_list[[1]][i],][[2]])
  gs1<-as.character(gs1)
  gs1<-strsplit(gs1,'\"')
  l1<-lengths(gs1)
  k1<-2:l1
  g1<-c()
  g1<-c(g1,gs1[[1]][k1])
  g1<-gsub(", ","NA",g1)
  #g1<-gsub("\\t ",",",g1)
  
  for (j in 1:len_path) {
    gs2<-unname(df[path_list[[1]][j],][[2]])
    gs2<-as.character(gs2)
    gs2<-strsplit(gs2,'\"')
    l2<-lengths(gs2)
    k2<-2:l2
    g2<-c()
    g2<-c(g2,gs2[[1]][k2])
    g2<-gsub(", ","NA",g2)
    #g2<-gsub("\\t ",",",g2)
    score=clusterSim(g1,g2,semData = hsGO2,measure = "Wang",combine = "BMA")
    #write.table(score,file = "path_score.txt",sep = "\t")
  }
  write.table(score,file = "path_score.txt",sep = "\t")
  
  #g1<-str_replace_all(g1,fixed(""),"")
  
  
  print(score)
  
}