remove(list=ls())
library(ggplot2)

rumex_dS_values <- read.csv(
  "C:/Users/mhibb/OneDrive - University of Toronto/Projects/rumex_phylogeny/allopolyploidy/Ks_plots/rumex_dS_values.csv", header=FALSE)

colnames(rumex_dS_values) <- c("Species", "dS")

#Need to remove some obvious outliers. Using the interquartile range method

detect_outlier <- function(x) {
  
  quant1 <- quantile(x, probs=.25, na.rm = TRUE)
  quant3 <- quantile(x, probs=.75, na.rm = TRUE)
  
  IQR = quant3 - quant1
  
  x > quant3 + (IQR*1.5) | x < quant1 - (IQR*1.5)
}

rumex_dS_values <- rumex_dS_values[!detect_outlier(rumex_dS_values[[2]]), ]
rumex_dS_values <- subset(rumex_dS_values, log(dS) > -5)

dSplot <- ggplot(rumex_dS_values, aes(x=dS)) + 
          geom_histogram() + facet_wrap(~Species, scales = "free")

log_dSplot <- ggplot(rumex_dS_values, aes(x=log(dS))) + 
  geom_histogram() + facet_wrap(~Species, scales = "free")