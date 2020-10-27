#!/bin/bash

set -e 

mkdir results

GENOME_FOLDER_NAME=$1
PFAM_FOLDER_NAME=$2

python create_list_files.py $GENOME_FOLDER_NAME $PFAM_FOLDER_NAME

PFAM_LIST=pfam_list.txt
GENOME_LIST=genomes_list.txt

while read -r genome; do

IFS="/";arrGEN=($genome); unset IFS;
genome_name=${arrGEN[-1]}

echo "Working with $genome_name."
mkdir results/$genome_name

while read -r pfam_id;do

IFS="/";arrPFAM=($pfam_id); unset IFS;
pfam_name=${arrPFAM[-1]}

output_file="$pfam_name-$genome_name"

hmmsearch $pfam_id $genome > results/$genome_name/$output_file

echo "Done for $output_file." 
done < $PFAM_LIST

echo "Results completed for $genome"

done < $GENOME_LIST


echo "Finished"