# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 13:37:52 2020

@author: Gurpinder
"""

import os
import sys

try:
    PROTEIN_INPUT = sys.argv[1]
    genome_file = open(PROTEIN_INPUT, "r")
    genome_file.close()
    print("file loaded.")
    #whole_genome = genome_file.readlines()
    file_name = str((PROTEIN_INPUT.split("\\")[-1]).split(".")[0])
except FileNotFoundError:
    print("File not found. exiting.")
        
CURRENT_DIR = os.getcwd()
DIVIDED_FILES_DIR = CURRENT_DIR + "\\Divided_files_" + file_name +"\\"
try:
    os.mkdir(path= DIVIDED_FILES_DIR)
except FileExistsError:
    print("{} already exists".format(DIVIDED_FILES_DIR))

print("\nSplitting the file\n")                


def file_splitter(file, out_dir, out_file_names, window=49):
    """
    Splits a large genome file into small files with 'window' number of sequences.

    Parameters
    ----------
    file : str, input file name
    out_dir : path str, Output directory for the splitted files
    out_file_names : str, name that will be given to the out-files
    window : int, optional
        maximum number of sequences in each file. The default is 49.

    Returns
    -------
    None.
    
    """
    seqs = {}
    count = 0
    Total_count = 0
    name_list_file = out_file_names+"_list.txt"
    name_list_f = open(name_list_file, "w")
    
    with open(file) as genome_file:
        whole_genome = genome_file.readlines()
        assert whole_genome[0].startswith(">")
    
    for line in whole_genome:
        if line.startswith(">"):
            meta = line
            seq = ""
            count += 1
            if count%window == 0:
                file_no = int(count/window)
                out_file_name = out_dir+ str(file_no) + "_" + out_file_names + ".fasta"
                with open(out_file_name, "w") as out_file:
                    for item in list(seqs.items()):
                        out_file.write(item[0] + item[1])
                Total_count += len(seqs)
                name_list_f.write(out_file_name+" ")
                print("{} file writen with {} sequences.".format(out_file_names+ "_" + str(file_no) + ".fasta", len(seqs)))
                seqs = {}
                                    
        else:
            seq = seq + line.replace("*", "")
            seqs[meta] = seq
            
    out_file_name = out_dir+ str(file_no + 1) + "_" + out_file_names + ".fasta"
    with open(out_file_name, "w") as out_file:
        for item in list(seqs.items()):
            out_file.write(item[0] + item[1])
    name_list_f.write(out_file_name)
    Total_count += len(seqs)
    name_list_f.close()
    print("{} file writen with {} sequences.".format(out_file_names+ "_" + str(file_no + 1) + ".fasta", len(seqs)))
    print("\n\n {} files, total sequences {}.".format(file_no + 1, Total_count))

file_splitter(PROTEIN_INPUT, DIVIDED_FILES_DIR, file_name)




