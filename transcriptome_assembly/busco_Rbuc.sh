#!/bin/bash

cd /ohta1/mark.hibbins/Assemblies/BUSCO/

#Conda environment for busco analysis
conda activate mark_Rbu_busco

#Run BUSCO
python3 /ohta1/mark.hibbins/.local/bin/busco -i /ohta1/mark.hibbins/Assemblies/Trinity/RBuc_Trinity/RBuc_trinity_5.Trinity.fasta --offline -l ./eudicots_odb10 -o RBuc5_eudicots -m transcriptome

python3 /ohta1/mark.hibbins/.local/bin/busco -i /ohta1/mark.hibbins/Assemblies/Trinity/RBuc_Trinity/RBuc_trinity_6.Trinity.fasta --offline -l ./eudicots_odb10 -o RBuc6_eudicots -m transcriptome
