#Rscript
library(tidyverse)
library(GENESPACE)
library(data.table)
wd <- "/ohta2/bianca.sacchi/genespaceBuc"
setwd(wd)
genomeRepo<-"/ohta2/bianca.sacchi/genespaceBuc/genomeRepo"

salkey<-readr::read_delim("/ohta2/Rumex/Dovetail_R_salicifolius/scaffolded_assembly/input_to_output.txt",col_names =c("old","new"),show_col_types = FALSE)
salkey<-salkey %>% mutate(fix=str_replace(old, "\\=", "\\_")) %>%
  mutate(.,fix=str_replace(fix, "\\;", "\\_")) %>%
  mutate(.,new =str_replace(new,"Scaffold_","")) %>% select(fix,new)
salkey<-as.data.frame(salkey)
## tx
fix<-c("LG1","LG3","LG5","LG2","LG4")
new<-c("A1","A2","A3","A4","XY")
texkey<-data.frame(fix,new)
mainkey<-rbind(salkey,texkey)

load(file="riparian/bucephalophorus_geneOrder_rSourceData.rda")
load(file="results/gsParams.rda")
chrs<-srcd$sourceData$chromosomes
scafs<-subset(chrs,genome == "bucephalophorus")[,2]
newscaf<-mutate(scafs,new =str_replace(chr, "scaffold_","")) %>% rename(.,fix = chr)
buckey<-data.frame(newscaf)
mainkey<-rbind(mainkey,buckey)
mainkey
invchr <- data.frame(
  genome = c("hap1","hap1","hap1"), 
  chr = c("A2","A4","X"))
PARfix <- data.table(
  genome = c("hap2","hap2","hap2",
        "hap2","hap2","hap2"),
  chr = c("Y1","Y1","Y1",
          "Y2","Y2","Y2"),
  start = c(0,64e6,272e6,
          0,121e6,159e6),
  end = c(64e6,272e6,345e6,
          121e6,159e6,350e6),
  color = c("darkorange","darkblue","#202020",
            "#202020","darkorange","darkblue"))

justPAR <- data.table(
  genome = c("hap1","hap1","hap1","hap1"),
  chr = c("X","X","X","X"),
  start = c(0,70e6,261e6,352e6),
  end = c(70e6,261e6,352e6,500e6),
  color = c("#6666FF","darkblue","darkorange","#C4645C"))

PAR <- data.table(
  genome = c("hap1","hap1","hap1","hap1"),
  chr = c("X","X","X","X"),
  start = c(0,71e6,261e6,367e6),
  end = c(71e6,261e6,367e6,500e6),
  color = c("#6666FF","darkblue","darkorange","#C4645C"))






ripDat<-plot_riparian(
  gsParam = gsParam,
  refGenome = "texas",
  forceRecalcBlocks = TRUE, 
  useOrder = TRUE,
  invertTheseChrs = invchr,
  chrLabFontSize = 6,
  highlightBed = PARfix,
  useRegions = TRUE,
  backgroundColor = NULL, 
  chrFill = "lightgrey",
  minChrLen2plot = 700,
  chrLabFun = function(x) matchmaker::match_vec(x,dictionary = mainkey))
  #customRefChrOrder = c("LG1","LG3","LG2","LG4","LG5"),
  #gapProp = 0.02,
  #chrExpand = 1.5) # changes height

ripDatRegion<-plot_riparian(
    gsParam = gsParam,
    refGenome = "texas",
    useOrder = TRUE,
    invertTheseChrs = invchr,
   chrLabFontSize = 6,
    chrFill = "lightgrey",
    minChrLen2plot = 500,
    chrLabFun = function(x) matchmaker::match_vec(x,dictionary = mainkey),
    customRefChrOrder = c("LG1","LG3","LG2","LG5","LG4"),
    highlightBed = justPAR)
ggsave("buc_slr_grey.pdf", width = 10,height=7)
getwd()

ripDat<-plot_riparian(
  gsParam = gsParam,
  refGenome = "texas",
  forceRecalcBlocks = TRUE, 
  useOrder = TRUE,
  invertTheseChrs = invchr,
  chrLabFontSize = 6,
  highlightBed = justPAR,
  useRegions = FALSE,
  chrFill = "lightgrey",
  minChrLen2plot = 500,
  chrLabFun = function(x) matchmaker::match_vec(x,dictionary = mainkey),
  customRefChrOrder = c("LG1","LG3","LG2","LG5","LG4"))
  #gapProp = 0.02,
  #chrExpand = 1.5) # changes height

ggsave("buc_slr_grey_blocks.pdf",width = 10,height=7)


myblks<-ripDat$blks
h12<-filter(myblks, genome1 == "hap1",genome2 == "hap2" & chr1 =="X" & (color == "darkblue"|color =="#6666FF"))
View(h12)
# par1/oldX boundary is within a block from 69-72MB
# looks fine

texh1<-filter(myblks, 
  genome1 == "hap1",
  genome2 == "texas" & 
  chr1 =="X" & color == "#6666FF")
View(texh1)

texh1reg<-filter(ripDatRegion$blks, 
  genome2 == "bucephalophorus",
  genome1 == "texas" & 
  chr1 =="LG4" & chr2 == "scaffold_3" & (color == "#6666FF"| color == "darkblue" | color == "#33333380"))
View(texh1reg)
View(myblks)

ripDat_all<-plot_riparian(
  gsParam = gsParam,
  refGenome = "texas",
  forceRecalcBlocks = TRUE, 
  useOrder = TRUE,
  invertTheseChrs = invchr,
  chrLabFontSize = 6,
  #highlightBed = justPAR,
  useRegions = TRUE,
  chrFill = "lightgrey",
  minChrLen2plot = 500,
  chrLabFun = function(x) matchmaker::match_vec(x,dictionary = mainkey),
  customRefChrOrder = c("LG1","LG3","LG2","LG5","LG4"))
  #gapProp = 0.02,
  #chrExpand = 1.5) # changes height
ggsave("txplot_labels.pdf",height = 7,width = 10)
#ggsave("bucplot_labels.pdf",height = 7,width = 10)
