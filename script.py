# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 18:27:00 2020

@author: Gurpinder
"""
import pandas as pd

output = pd.read_csv("Output_allfam_csv.csv")

def reader(path):
    seqs = {}
    with open(path, "r") as f:
        Lines = f.readlines()
        for line in Lines:
            if line.startswith(">"):
                accession = line[1:]
                seq = ""
            else:
                seq = seq + line
            seqs[accession] = seq
    return seqs

fasta = reader('allergens_Allfam.fasta')

headers = [h.rstrip() for h in output['1']]
pf_ids = output['2']
fam_names = output['3']

combiner = {}
for i in range(len(headers)):
    if headers[i] not in list(combiner.keys()):
        combiner[headers[i]] = [(pf_ids[i], fam_names[i])]
    else:
        combiner[headers[i]].append((pf_ids[i], fam_names[i]))

fasta_new = {}        
for original_header in list(fasta.keys()):
    if original_header[:-1] in list(combiner):
        extended_str = ''
        for i in range(len(combiner[original_header[:-1]])):
            extended_str = extended_str + ' '.join(combiner[original_header[:-1]][i]) + ", "
        new_header = original_header[:-1] + ' (' + extended_str[:-2] + ")\n"
    else:
        new_header = original_header[:-1] + "(None)" + "\n"
        
    fasta_new[new_header] = fasta[original_header]
                                         
with open("Allergens_Allfam_w_HMMER_fams.fasta", "w") as out_f:
    for allergen in list(fasta_new.keys()):
        out_f.write(">"+allergen+fasta_new[allergen])
        
    