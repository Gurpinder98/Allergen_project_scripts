# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 16:48:07 2020

@author: Gurpinder
"""
######## Change these file names if needed #############
file_name = "domtblout_03"
file_name_2 = "allergens_Allfam.fasta"
####################################################

file_name_3 = "split_domains_"+file_name_2
file_name_4 = "No_domains_found_"+file_name_2

def reader(path):
    """
    reads fasta file and returns it as a dictionary
    Note: removes ">" or any other information from header line except accession
    removes "\n" from sequences.
    """
    seqs = {}
    with open(path, "r") as f:
        Lines = f.readlines()
        for line in Lines:
            if line.startswith(">"):
                accession = line.split(" ")[0][1:]
                seq = ""
            else:
                seq = seq + line.replace("\n", "")
            seqs[accession] = seq
    return seqs

def new_line_inserter(seq, line_length=70):
    """
    Returns a new string with \n added after every line_length number of residues. 
    """
    splits = [seq[i:i+line_length] for i in range(0, len(seq), line_length)]    
    return "\n".join(splits)

def hmmer_domtblout_parser(file_name):
    """
    parses domtblout output format of hmmsearch.
    retuns a list of headers and a list containing start stop values of domains in file
    """
    with open(file_name, "r") as in_f:
        lines = in_f.readlines() #read all lines from the file
        
    cleaned_lines = [] 
    for line in lines:
        if line.startswith("#") != True:
            cleaned_lines.append(line.split()) #remove all lines that start with #

    header_lines = []
    start_stop = []

    for i in range(len(cleaned_lines)):
        line = cleaned_lines[i]
        #header string format = "accession, _ , domain number, Allfam information, [seq length, (slice)] (pfam_id, pfam_name )  
        header_string = "{}_{} {} [{}, ({}, {})] ({}, {})".format(line[0], line[9], ' '.join(line[22:]), line[2], line[19], line[20], line[4], line[3])
        header_lines.append(header_string) #header string for new fasta file
        start_stop.append((line[19], line[20])) #corresponding start stop values
    
    return header_lines, start_stop 


allergen_seqs = reader(file_name_2) #get allergen sequences and save them as dictionary
header_lines, start_stop = hmmer_domtblout_parser(file_name)  # parse hmmsearch domtblout output file
new_fasta = {} 

for i in range(len(header_lines)):
    accession = header_lines[i].split()[0][:-2] #get accession from the header line    
    full_sequence = allergen_seqs[accession] #get allergen sequence corresponding to the accession of the headerline
    
    #splitting the seq: "-1" because python indexes strings from 0 not 1
    #no "-1" for the stop position because python doesn't include that number of residue in the slice. eg. if end value is 348, python will only take upto 347. 
    #so -1 is not needed.
    seq_split = full_sequence[int(start_stop[i][0])-1: int(start_stop[i][1])] #corresponding i-th start_stop indexes
    
    new_fasta[header_lines[i]] = new_line_inserter(seq_split)+"\n"

#write to the file    
with open(file_name_3, "w") as out_f:
    for header in list(new_fasta.keys()):
        out_f.write(">"+header+"\n"+new_fasta[header]) 
    
# take out sequences with no domains found.
accessions = [header.split()[0][:-2] for header in header_lines] #list of all accessions in new fasta file - contains duplicates

with open(file_name_4, "w") as out_f2:
    counter = 0    
    for seq_accession in list(allergen_seqs.keys()): #check every accession in allergen file
        if seq_accession not in accessions: #if it is not in accessions
            counter+=1
            out_f2.write(">"+seq_accession+"\n"+new_line_inserter(allergen_seqs[seq_accession])+"\n")
  
######### print helpful stats? ############################    
from collections import Counter #to count number of unique accessions in accessions.
print("""
      {} sequences processed.\n{} Domains found in {} sequences, {} sequences had no hits.\n
      """.format(len(allergen_seqs), len(header_lines),len(Counter(accessions)), counter))

    
    



        