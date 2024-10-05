getwd()
setwd("/home/ksrao/saikat/workflow_R/diabetes_GSE64998_wgcna/")
library(WGCNA)
datMicro=read.csv("_probe_to_geneid_without_filter.csv")
datMicro=datMicro[!is.na(datMicro$GeneSymbol),]
datMicro[2:2,]
ArrayName=names(data.frame(datMicro[,-1]))
ArrayName
GeneName=datMicro$GeneSymbol
GeneName
datExpr=data.frame(t(datMicro[,-1]))
names(datExpr)=datMicro[,1]
dimnames(datExpr)[[1]]=names(data.frame(datMicro[,-1]))
meanExpressionByArray=apply(datExpr,1,mean,na.rm=T)
NumberMissingByArray=apply(is.na(data.frame(datExpr)),1,sum)
sizeGrWindow(9,5)
barplot(meanExpressionByArray,xlab="Sample",ylab="Mean expression", main= "Mean expression across samples", names.arg=c(1:50),cex.names=0.7)
KeepArray=NumberMissingByArray<500
table(KeepArray)
datExpr=datExpr[KeepArray,]
ArrayName[KeepArray]
NumberMissingByGene=apply(is.na(data.frame(datExpr)),2,sum)
summary(NumberMissingByGene)
variancedatExpr=as.vector(apply(as.matrix(datExpr),2,var, na.rm=T))
no.presentdatExpr=as.vector(apply(!is.na(as.matrix(datExpr)),2,sum))
table(no.presentdatExpr)
KeepGenes=variancedatExpr>0 & no.presentdatExpr>=4
table(KeepGenes)
datExpr=datExpr[,KeepGenes]
GeneName=GeneName[KeepGenes]
sizeGrWindow(9,5)
plotClusterTreeSamples(datExpr = datExpr)
GS1=as.numeric(cor(datExpr,use = "p"))
## defining a weighted gene coexpression network
#defining the adjacency matrix using soft thresholding with beta=6
ADJ1=abs(cor(datExpr, use = "p"))^6
#k=softConnectivity(datExpr = datExpr, power = 6)
#net=blockwiseModules(datExpr = datExpr, power = 6, TOMType = "unsigned", minModuleSize = 30, reassignThreshold = 0, mergeCutHeight = 0.25, numericLabels = T, pamRespectsDendro = F, saveTOMs = T, saveTOMFileBase = "parkHumanTom", verbose = 3)
## topological overlap calculations

TOM=TOMsimilarityFromExpr(datExpr,power = 6)
