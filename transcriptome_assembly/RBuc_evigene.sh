#!/bin/bash

#Set path to cd-hit-est

export PATH=$PATH:/ohta1/apps/cdhit

cd /ohta1/mark.hibbins/Assemblies/evigene_tr2aacds4_bucephalophorus/

#1. preprocess transcripts as input
perl /ohta1/joanna.rifkin/evigene/scripts/rnaseq/trformat.pl -pre R_bucephalophorus -out R_bucephalophorus.tr -log -in /ohta1/mark.hibbins/Assemblies/Trinity/RBuc_Trinity/R_bucephalophorus_master_trinity.fasta

#2. run tr2aacds4.pl
perl /ohta1/joanna.rifkin/evigene/scripts/prot/tr2aacds4.pl -logfile -cdnaseq R_bucephalophorus.tr

#3. select main transcripts
perl -ne 'if(/^>(\S+)/){ $id=$1; $ok=($id=~m/t1$/); } print if $ok;' R_bucephalophorus.okay.mrna > R_bucephalophorus.t1okay.mrna
