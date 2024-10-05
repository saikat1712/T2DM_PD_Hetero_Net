setwd("/home/ksrao/saikat/workflow_R/parkinson_gene_expression_GSE99039/")
library(affy)
library(limma)
library(annotate)
library(hgu133plus2.db)
library(GEOquery)

##Making phenodata from series matrix file

filenm= "/home/ksrao/saikat/workflow_R/parkinson_gene_expression_GSE99039/GSE99039_series_matrix.txt.gz"
gse<- getGEO(filename = filenm)
class(gse)
names(gse)
class(gse)
str(gse)
colnames(pData(gse))
pdata<-as.data.frame(pData(gse), stringsAsFactors=FALSE)
pdata<-pdata[, c("title","geo_accession","disease label:ch1","Sex:ch1")]
pdata<-pdata[order(rownames(pdata)),]
write.table(pdata, file="_SelectPhenoData.txt", sep="\t", quote=F,row.names = F,col.names = T)
## unzipping CEL files
untar("GSE99039_RAW.tar",exdir = "data")
cels=list.files("data/",pattern="CEL")
setwd("/home/ksrao/saikat/workflow_R/parkinson_gene_expression_GSE99039/data")
dat<- ReadAffy(filenames = cels,compress = T)
show(dat)
class(dat)
dim(dat)
str(dat)
annotation(dat)
head(featureData(dat))
pData(dat)
## Mapping CEL files to phenodata
setwd("/home/ksrao/saikat/workflow_R/parkinson_gene_expression_GSE99039")
pheno<-read.table("/home/ksrao/saikat/workflow_R/parkinson_gene_expression_GSE99039/_SelectPhenoData.txt",sep="\t",header = T,colClasses = c("character","character","character"))
str(pheno)
summary(pheno)
table(pheno$disease.label.ch1)
table(pheno$title)
table(pheno$geo_accession)
##removing suffix .CEL from sample to match the phenodata rownames
sampleNames(dat)=sub("\\.CEL.gz$","",sampleNames(dat))
sampleNames(dat)=sub("_.*", "", sampleNames(dat))
sampleNames(dat)
rownames(pData(dat))

if (all(rownames(pData(dat)) == pheno$geo_accession)) {
  print("You're good, go ahead!")
  pheno <- merge(pData(dat), pheno, by.x = 0, by.y = "geo_accession", sort = FALSE)
  rownames(pheno) <- pheno[, "Row.names"]
  pData(dat) <- pheno
} else {
  print("Check order of rows in pData(object) and pheno data provided!")
}
pData(dat)
## create shorter descriptive levels and labels
pheno$disease.label.ch1<-sub(" ","_",pheno$disease.label.ch1)
pheno$disease.label.ch1<-sub("-","_",pheno$disease.label.ch1)
pheno$disease.label.ch1
pData(dat)$sample.levels <- pheno$disease.label.ch1
table(pData(dat)$sample.levels)
pData(dat)
#cbind(as.character(pData(dat)$description), pData(dat)$sample.levels, pData(dat)$sample.labels)
dat.rma<-rma(dat)
class(dat.rma)
pData(dat.rma)
annotation(dat.rma)
head(featureData(dat.rma))
dim(dat.rma)
write.table(exprs(dat.rma), file="_RMA_Norm_Filter.txt", sep="\t", quote=FALSE)
write.table(exprs(dat.rma), file="_RMA_Norm_Filter.csv", quote=FALSE)
###Filtering the data
library(genefilter)
dat.filter<-nsFilter(dat.rma,remove.dupEntrez = F, var.filter = F, filterByQuantile = F ,feature.exclude = "^AFFX")$eset
dim(dat.filter)
pData(dat.filter)$sample.levels<-as.factor(pData(dat.filter)$sample.levels)
#control<-grep("AFFX",rownames(exprs(dat.filter)))
#dat.rma<-dat.rma[-control,]
#dim(dat.rma)
#dat.filter
#probes=row.names(dat.filter)
#probes

##DGE Analysis

my.design<-model.matrix(~0 + sample.levels, pData(dat.filter))
my.design
rownames(my.design)<-pData(dat.filter)$sample.levels
my.design
colnames(my.design)<-levels(pData(dat.filter)$sample.levels)
my.design
colnames(my.design)
##determine the average effect (coefficient) for each treatment
my.fit<-lmFit(exprs(dat.filter),my.design)
my.fit

##Making comparisons(contrasts) between samples

##specify the contrast of interest using the levels from the design matrix

my.contrasts <- makeContrasts(CpD = CONTROL-PD_DEMENTIA, CapD = CONTROL-ATYPICAL_PD,Ccbd= CONTROL-CBD, Cdrd= CONTROL - DRD, Cdd5= CONTROL-DRD_DYT5,Cgun=CONTROL-GENETIC_UNAFFECTED,Cgpd=CONTROL-GENETIC_UNAFFECTED,Chdba=CONTROL-HD_HD_BATCH,Cipd=CONTROL-IPD,Cms=CONTROL-MSA,Cps=CONTROL-PSP,Cvas=CONTROL-Vascular_dementia ,levels = my.design)
my.contrasts
colnames(my.contrasts)
fit2<-contrasts.fit(my.fit,my.contrasts)
fit2<-eBayes(fit2,proportion = 0.01,trend = T)
plotSA(fit2)
#fit2<-eBayes(fit2[fit2$Amean>5,],trend = T)
#plotSA(fit2)
rownames(fit2)
library(hgu133plus2.db)
columns(hgu133plus2.db)
tg<-topTable(fit2, coef = "CpD",number=Inf, resort.by = "logFC",genelist = rownames(fit2))
tg
sym<-mget(tg$ID, hgu133plus2SYMBOL, ifnotfound = NA)
#combine gene anotations with raw data
#rma_entrez=cbind(probes,SYMBOL=unlist(sym),dat.filter)
#rma_entrez
#write.table(rma_entrez, file = "_rma_entrez_expression.txt",quote = F, sep='\t',row.names = F, col.names = T)
tganno<-cbind(SYMBOL=unlist(sym), tg, stringsAsFactors=F )
tganno
str(tganno)
volcanoplot(fit2)
write.table(tganno,file = "differentially_expressed_genes.txt", sep = "\t", quote = T)
tganno_1=tganno[,c(1,2,3,6)]
write.csv(tganno_1,file = "diffrential_genes.csv")

##### Making the gene to sample level expression file ####################

Probes_ID=row.names(dat.rma)
GeneSymbol=unlist(mget(Probes_ID,hgu133plus2SYMBOL, ifnotfound = NA))
dat.rma_without_filter=cbind(Probes_ID,GeneSymbol,exprs(dat.rma))
k=2:560
dat.rma_without_filter=dat.rma_without_filter[,c(k)]
write.csv(dat.rma_without_filter,file = "_probe_to_geneid_without_filter.csv",row.names = F)
