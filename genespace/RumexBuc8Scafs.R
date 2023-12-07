#Rscript

## redoing genespace from beginning with just the 8 largest scaffolds. Other analyses suggest that scaffolds 9 & 10 are perhaps due to heterozygous inversions. Genespace creator recommends against removing these in the plot, rather to remove them upstream (e.g. before the orthofinder step).

##---- load dependencies! ----
library(tidyverse)
library(GENESPACE)
library(data.table)
## --- setwd ---
wd <- "/ohta2/bianca.sacchi/genespaceBuc/"
setwd(wd)
## --- run GENESPACE ---
## parsedPaths
genomeRepo <-"/ohta2/bianca.sacchi/genespaceBuc/genomeRepo"
parsedPaths <- parse_annotations(
     rawGenomeRepo = genomeRepo,
     genomeDirs = c("salicifolius","hap1_unfiltered","hap2_unfiltered","texas","buc_subset"),
     genomeIDs = c("salicifolius","hap1","hap2","texas","bucephalophorus"),
     gffString = "gff",
     faString = "fasta",
     presets = "none",
     genespaceWd = wd,
     gffIdColumn = "ID",
     gffStripText = "ID=",
     headerEntryIndex = 1,
     headerSep = " ",
     headerStripText = "-RA")


## init genespace
gpar <- init_genespace(
  genomeIDs = c("texas","hap1","hap2","salicifolius","bucephalophorus"),
  onewayBlast = TRUE,
  ploidy=1,
  wd = wd,
  path2mcscanx ="~/bin/MCScanX-master")

out <- run_genespace(gpar, overwrite = T)

## rda will be save in results for additional plotting
