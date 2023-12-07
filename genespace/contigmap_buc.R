#R script

# using GENESPACE's contig map function on the salicifolius genome

###################
library(GENESPACE)
suppressPackageStartupMessages(library(data.table))
suppressPackageStartupMessages(library(Biostrings))
suppressPackageStartupMessages(library(tidyverse))

## hap1
faFile <- "/ohta2/Rumex/Dovetail_R_bucephalophorus/final_primary_assembly/buc.fasta"
dnaSS <- Biostrings::readDNAStringSet(faFile)
# just the main scaffolds
ns <- names(dnaSS)

scaflist<-list("scaffold_1","scaffold_2",
           "scaffold_3","scaffold_4","scaffold_5",
           "scaffold_6","scaffold_7","scaffold_8",
           "scaffold_9","scaffold_10")


# get list of scaffolds to keep and rename
#isalkey<-readr::read_delim("/ohta2/Rumex/Dovetail_R_salicifolius/scaffolded_assembly/input_to_output.txt",
#                           col_names =c("old","new"),
#                           show_col_types = FALSE)
#salkey<-as.data.frame(salkey)
# renaming function
# keep only main 10 scaffs (old names)
#dnaSS <- dnaSS[ns]
# rename dnaSS object
ns<-ns[ns%in%scaflist]
dnaSS <- dnaSS[ns]
### below not necessary :)
# -- parse the chromosome names so they are better for plotting ...
plantTelomereKmers <- "TTTAGGG"
genomeGrs <- find_contigsGapsTelos(
  dnass = dnaSS,
  teloKmers = plantTelomereKmers,
  maxDistBtwTelo = 500,
  minTeloSize = 1000,
  minTeloDens = .9,
  maxDist2end = 50e3,
  minChrSize = 1e6,
  minContigGapSize = 1000)

print(lapply(genomeGrs, head))
pdf("contigmap_telo_buc.pdf")
plot_contigs(
  cgt = genomeGrs,
  nColors = 20,
  palette = viridis::viridis)
dev.off()
