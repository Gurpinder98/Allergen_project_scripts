#!/usr/bin/bash

set -x -e

INPUT_FOLDER_NAME=$1
OUTPUT_FOLDER_NAME=$2
mkdir ${OUTPUT_FOLDER_NAME}
all_files=( $(ls ${INPUT_FOLDER_NAME} ) )
counter=0
for file in ${all_files[@]}; do
	input_full_name_file="${INPUT_FOLDER_NAME}/${file}";
	output_full_name_file="${OUTPUT_FOLDER_NAME}/${file}";
	./LIgE -i ${input_full_name_file} -m pro -M 'RF' -t 0.5 -BT 0.7 -o ${output_full_name_file}; #change the parameters HERE!
	echo "done for ${file}";
	counter+=1
	done
echo "done. ${counter} files writen to ${OUTPUT_FOLDER_NAME}"



