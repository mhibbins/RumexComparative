remove(list=ls())
library(mclust)

rumex_dS_values <- read.csv(
  "C:/Users/mhibb/OneDrive - University of Toronto/Projects/rumex_phylogeny/allopolyploidy/Ks_plots/rumex_dS_values.csv", header=FALSE)

colnames(rumex_dS_values) <- c("Species", "dS")

detect_outlier <- function(x) {
  
  quant1 <- quantile(x, probs=.25, na.rm = TRUE)
  quant3 <- quantile(x, probs=.75, na.rm = TRUE)
  
  IQR = quant3 - quant1
  
  x > quant3 + (IQR*1.5) | x < quant1 - (IQR*1.5)
}

rumex_dS_values <- rumex_dS_values[!detect_outlier(rumex_dS_values[[2]]), ]
rumex_dS_values$dS <- log(rumex_dS_values$dS)
rumex_dS_values[sapply(rumex_dS_values, is.infinite)] <- NA
rumex_dS_values <- na.omit(rumex_dS_values)

#Trying a cutoff to eliminate very low dS outliers
rumex_dS_values <- subset(rumex_dS_values, dS > -5)

ace <- rumex_dS_values[rumex_dS_values$Species == "R_acetosella",]$dS
amu <- rumex_dS_values[rumex_dS_values$Species == "R_amurensis",]$dS
buc <- rumex_dS_values[rumex_dS_values$Species == "R_bucephalophorus",]$dS
has <- rumex_dS_values[rumex_dS_values$Species == "R_hastatulus",]$dS
pau <- rumex_dS_values[rumex_dS_values$Species == "R_paucifolius",]$dS
rot <- rumex_dS_values[rumex_dS_values$Species == "R_rothschildianus",]$dS
sag <- rumex_dS_values[rumex_dS_values$Species == "R_sagittatus",]$dS
sal <- rumex_dS_values[rumex_dS_values$Species == "R_salicifolius",]$dS
scu <- rumex_dS_values[rumex_dS_values$Species == "R_scutatus",]$dS
thy <- rumex_dS_values[rumex_dS_values$Species == "R_thyrsiflorus",]$dS
tri <- rumex_dS_values[rumex_dS_values$Species == "R_trisetifer",]$dS
buck <- rumex_dS_values[rumex_dS_values$Species == "F_tataricum",]$dS

ace_BIC <- mclustBIC(ace)
amu_BIC <- mclustBIC(amu)
buc_BIC <- mclustBIC(buc)
has_BIC <- mclustBIC(has)
pau_BIC <- mclustBIC(pau)
rot_BIC <- mclustBIC(rot)
sag_BIC <- mclustBIC(sag)
sal_BIC <- mclustBIC(sal)
scu_BIC <- mclustBIC(scu)
thy_BIC <- mclustBIC(thy)
tri_BIC <- mclustBIC(tri)
buck_BIC <- mclustBIC(buck)

buck_plot <- plot(pau_BIC)
