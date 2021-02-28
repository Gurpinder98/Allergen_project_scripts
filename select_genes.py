# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 13:34:43 2020

@author: Gurpinder
"""
import pandas as pd

"""

def reader(path):
    
    Reads a file containing multiple fasta sequences and outputs them as a dictionary
    input:
        path: file path to open
    returns:
        seqs: a dictionary with sequence name and sequence itself as key, value pairs.
    
    seqs = {}
    with open(path, "r") as f:
        Lines = f.readlines()
        for line in Lines:
            if line.startswith(">"):
                accession = line.split(" ")[0][1:]
                seq = ""
            else:
                seq = seq + line.replace("*", '')
            seqs[accession] = seq
    return seqs

selected = pd.read_csv("Anther-Pollen-Diff-gene-expression-significant-log2fold.csv", sep = "\t")
genes = list(selected["gene_id"])

FASTA_file = reader("Os-Nipponbare-Reference-IRGSP-7_0.fasta")
FASTA_ids = list(FASTA_file.keys())

Selected_seqs = []
for accession in FASTA_ids:
    if accession[:-2] in genes:
        Selected_seqs.append(accession)

to_write = ""
for seq in Selected_seqs:
    to_write = to_write + ">" + seq + "\n" + FASTA_file[seq]
    
with open("Selected.fasta", "w") as out_f:
    out_f.write(to_write)
           
        
"""        

"""       
all_results = pd.read_csv("C_combined.csv")

all_results_clean = all_results.drop(['Sequence Length', 'Gluten allergens (# of Q-repeats)', '# of 3x6-mer overlaps', 'Known allergen hit name', '% identity linear 80 aa window', '% identity 3D epitope', 'Comment'], axis = 1)

proteins = list(all_results_clean["Protein"])

proteins_clean = []
for protein in proteins:
    proteins_clean.append(protein.split(" ")[0])


"""

all_results = pd.read_csv("Results_600_on.csv")

genes_all = [protein[:-2] for protein in list(all_results["Protein"])]

selected = pd.read_csv("Anther-Pollen-Diff-gene-expression-significant-log2fold.csv", sep = "\t")
genes = list(selected["gene_id"])


left_outs = []
for gene in genes:
    if gene not in genes_all:
        left_outs.append(gene)

def reader(path):
    seqs = {}
    with open(path, "r") as f:
        Lines = f.readlines()
        for line in Lines:
            if line.startswith(">"):
                accession = line.split(" ")[0][1:]
                seq = ""
            else:
                seq = seq + line.replace("*", '')
            seqs[accession] = seq
    return seqs


FASTA_file = reader("Os-Nipponbare-Reference-IRGSP-7_0.fasta")
FASTA_ids = list(FASTA_file.keys())

to_write = []
for ID in FASTA_ids:
    if ID[:-2] in left_outs:
        to_write.append(ID)
        

write = ""
for seq in to_write:
    write = write + ">" + seq + "\n" + FASTA_file[seq]
    
with open("Selected_jas.fasta", "w") as out_f:
    out_f.write(write)
       
        
        