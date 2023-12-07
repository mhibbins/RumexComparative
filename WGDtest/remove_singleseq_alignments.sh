#!/bin/bash

for file in aa_MUSCLE_alignments/*; 
do 
seqcount=$(fgrep -o ">" $file | wc -l) 
if [$seqcount -eq 1] 
then 
echo "Removing $file" 
rm $file 
fi 
done
