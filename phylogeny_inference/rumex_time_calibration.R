library(ape)

rumex_tree <- read.tree("C:/Users/mhibb/OneDrive - University of Toronto/Projects/rumex_phylogeny/phylogeny_inference/iqtree_results/rumex_iqtree_resolved.tree")

#Nodes to set dates for 
node <- c(
  getMRCA(rumex_tree, tip = c("R_salicifolius","R_hastatulus")),
  getMRCA(rumex_tree, tip = c("R_rothschildianus","R_hastatulus")),
  getMRCA(rumex_tree, tip = c("R_sagittatus","R_hastatulus"))
)

#Min and max age for each node 
age.min <- c(14, 10.8, 13.77) 
age.max <- c(23, 10.8, 13.77)

soft.bounds <- c(TRUE,FALSE,FALSE)

calib <- data.frame(node, age.min, age.max, soft.bounds)

#calib <- ape::makeChronosCalib(rumex_tree, node = "root", age.max = 23)

#Correlated: 

corr_timetree <- ape::chronos(rumex_tree, lambda = 1, model = "correlated",
                              calibration = calib, control = chronos.control())

#Discrete: 

dis_timetree <- ape::chronos(rumex_tree, lambda = 1, model = "Discrete",
                              calibration = calib, control = chronos.control())

#Relaxed: 

rel_timetree <- ape::chronos(rumex_tree, lambda = 1, model = "Relaxed",
                             calibration = calib, control = chronos.control())

#Discrete model tree has the lowest PHIIC and looks the most sensible

ape::write.tree(dis_timetree, "rumex_timecalibrated.newick")
