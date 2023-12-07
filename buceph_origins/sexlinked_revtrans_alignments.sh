#!/bin/bash

filenum=$(ls sexlinked_AA_alignments/ | wc -l)
filecounter=0

for protfile in sexlinked_AA_alignments/* 
do 
orthogroup=$(echo $protfile | cut -d '/' -f2 | cut -d '_' -f1)
seqfile=$(find ./usable_orthogroup_fastas/ -name "*$orthogroup*" -print)
echo $seqfile
echo $protfile
revtrans.py $seqfile $protfile sexlinked_codon_alignments/"$orthogroup"_codon_aligned.fa
filecounter=$((filecounter+1))
echo "Finished file $filecounter out of $filenum"  
done
