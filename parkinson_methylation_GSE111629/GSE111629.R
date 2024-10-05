library(minfi)
library(limma)
library(IlluminaHumanMethylation450kanno.ilmn12.hg19)
library(IlluminaHumanMethylation450kmanifest)
library(missMethyl)
library(DMRcate)
library(ExperimentHub)
library(GEOquery)
library(RColorBrewer)
library(stringr)
setwd("/home/ksrao/saikat/workflow_R/parkinson_methylation_GSE111629/")
#source("/home/ksrao/saikat/workflow_R/parkinson_methylation_GSE111629/GEOpatch.r")
untar("GSE111629_RAW.tar",exdir = "idat_data")
list.files("idat_data/",pattern= "idat")
head(list.files("idat_data/",pattern= "idat"))
idatFiles<- list.files("idat_data/",pattern="idat.gz$",full=T)
sapply(idatFiles,gunzip,overwrite=T)
rm(idatFiles)
#get the 450k annotation data
anno450k<- getAnnotation(IlluminaHumanMethylation450kanno.ilmn12.hg19)
head(anno450k)
#targets<-read.metharray.sheet(idatFiles,pattern = "SampleSheet.csv")
rgSet<-read.metharray.exp("/home/ksrao/saikat/workflow_R/parkinson_methylation_GSE111629/idat_data/")
rgSet
pData(rgSet)
#phenodata retrieving

filenm1="/home/ksrao/saikat/workflow_R/parkinson_methylation_GSE111629/GSE111629_series_matrix.txt.gz"
geoMat<-getGEO(filename = filenm1)
pdata<-as.data.frame(pData(geoMat), stringsAsFactors=FALSE)
pdata
pdata<-pdata[, c("title","geo_accession","characteristics_ch1.2","characteristics_ch1.3")]
pdata
names(pdata)[c(4,3)]<-c("group_status","tissue_type")
pdata$group_status<-sub(" ","",pdata$group_status)
pdata$group_status<-sub("^diseasestate:","",pdata$group_status)
pdata$tissue_type<-sub(" ","",pdata$tissue_type)
pdata$tissue_type<-sub("^tissuetype: ","",pdata$tissue_type)
pdata$group_status
pdata$ID<-paste(pdata$group_status,pdata$tissue_type,sep = ".")
pdata$ID
## Mapping rgSet with phenodata

sampleNames(rgSet)<-sub(".*_9","9",sampleNames(rgSet))
sampleNames(rgSet)<-pdata$ID
rgSet

#rownames(pdata)<-pdata$title
#pdata<-pdata[sampleNames(rgSet),]
#pData(rgSet)<-pdata
#rgSet
# calculate the detection p-values

detP<-detectionP(rgSet)
head(detP)

qcReport(rgSet, sampNames =pdata$ID, sampGroups = pdata$group_status, pdf = "qcReport.pdf")

##remove the poor quality samples

keep<-colMeans(detP)< 0.05
rgSet<-rgSet[,keep]
rgSet

#remove poor quality samples from pdata data

pdata<-pdata[keep,]
pdata

# remove poor quality samples from detection p-value table

detP<-detP[,keep]
dim(detP)

# normalize the data; this results in a GenomicRatioSet object

mSetSq<-preprocessFunnorm(rgSet,nPCs = 0,bgCorr = T,sex = NULL,dyeCorr = T,verbose = T)

# create a MethylSet object from the raw data for plotting

mSetRaw<-preprocessRaw(rgSet)

#ensure probes are in the same order in the mSetSq and detP object

detP<-detP[match(featureNames(mSetSq),rownames(detP)),]

# remove any probes that failed in one or more samples

keep<- rowSums(detP < 0.01)==ncol(mSetSq)
table(keep)

mSetSqFlt<- mSetSq[keep,]
mSetSqFlt

# remove probes with SNPs at CpG site

mSetSqFlt<-dropLociWithSnps(mSetSqFlt)
mSetSqFlt

# calculate M-values for statistical analysis

mVals<-getM(mSetSqFlt)
head(mVals[,1:5])

# calculate Beta values

bVals<- getBeta(mSetSqFlt)
head(bVals)

# this is the factor of interest

diseaseStatus<-factor(pdata$group_status)
diseaseStatus
diseaseStatus<-as.factor(make.names(diseaseStatus))#relebeling the levels of pdata
diseaseStatus
# this is the individual effect that we need to account for

individual<- factor(pdata$tissue_type)

# use the above to create the design matrix

design<-model.matrix(~0 + diseaseStatus + individual, data = pdata)
colnames(design)<-c(levels(diseaseStatus), levels(individual)[-1])
colnames(design)


# fit the linear model

fit<-lmFit(mVals, design)
fit

# create the contrast matrix for specific comparisions

contMatrix<- makeContrasts(X.Metastasis-X.Normal,X.Metastasis-X.PIN,X.Metastasis-X.Tumor,X.Normal-X.PIN,X.Normal-X.Tumor,X.PIN-X.Tumor, levels = design)
contMatrix
colnames(contMatrix)

#fit the contrats

fit2<-contrasts.fit(fit,contMatrix)
fit2<-eBayes(fit2)

# look at the numbers of DM CpGs at FDR < 0.05

summary(decideTests(fit2))

#get the table for the contrast (Normal-Tumor)

anno450kSub<-anno450k[match(rownames(mVals),anno450k$Name),c(1:4,12:19,24:ncol(anno450k))]
DMPs<-topTable(fit2, num=Inf, coef = 5, genelist = anno450kSub,sort.by = "p")
head(DMPs)
write.table(DMPs, file = "DMPs.txt",sep = "\t",row.names = F)
#plotting top 4 differntially methylated CpGs

par(mfrow=c(2,2))
sapply(rownames(DMPs)[1:4], function(cpg){
  plotCpg(bVals,cpg = cpg,pheno = pdata$group_status,ylab = "Beta values")
})

# differential methylation analysis of regions
#library(DMRcate)
myAnnotation<-cpg.annotate(object = mVals, datatype="array",what = "M",analysis.type = "differential", design = design,contrasts=T,cont.matrix = contMatrix ,coef ="X.Normal - X.Tumor" , arraytype ="450K" )
str(myAnnotation)
DMRs<-dmrcate(myAnnotation, lambda = 1000, C=2)
#extractRanges(DMRs)
library(httr)    
set_config(use_proxy(url="172.16.2.30",port=8080))
results.ranges<-extractRanges(DMRs, genome = "hg19")
results.ranges
write.table(results.ranges,file = "DMR_all.txt",sep = "\t")
#visualizing and grouping variables and colors
pal<-brewer.pal(8,"Dark2")
groups<-pal[1:length(unique(pdata$group_status))]
names(groups)<-levels(factor(pdata$group_status))
cols<-groups[as.character(factor(pdata$group_status))]
#draw plot for top DMRs
par(mfrow=c(1,1))
DMR.plot(ranges = results.ranges,dmr = 2,CpGs = bVals,phen.col = cols,what = "Beta",arraytype = "450K",genome = "hg19")
