import os
import sys

genome_file_original = sys.argv[1]
result_file_allergens= sys.argv[2]
out_file = sys.argv[3]

def reader(path):
    """
    Reads a file containing multiple fasta sequences and outputs them as a dictionary
    input:
        path: file path to open
    returns:
        seqs: a dictionary with sequence name and sequence itself as key, value pairs.
    """
    seqs = {}
    with open(path, "r") as f:
        Lines = f.readlines()
        for line in Lines:
            if line.startswith(">"):
                accession = line.split(" ")[0][1:]
                seq = ""
            else:
                seq = seq + line
            seqs[accession] = seq
    return seqs


def Sequence_selector(Allergens_predicted, Proteome_file):
    
    selected_seqs = {}
    with open(Allergens_predicted, "r") as allergen_file:
        lines = allergen_file.readlines()
    selected_seq_names_strong = [line.split(",")[0].split(" ")[0][1:].replace('"', '') for line in lines if 'strong evidence' in line]
    selected_seq_names_weak = [line.split(",")[0].split(" ")[0][1:].replace('"', '') for line in lines if 'weak evidence' in line]
    selected_seq_names = selected_seq_names_strong + selected_seq_names_weak
    print("{} had {} allergen sequences ({} strong + {} weak).".format(Allergens_predicted, len(selected_seq_names), len(selected_seq_names_strong), len(selected_seq_names_weak)))
    whole_proteome = reader(Proteome_file)
    for seq in list(whole_proteome.keys()):
        if seq in selected_seq_names:
            selected_seqs[seq] = whole_proteome[seq]
    print(len(selected_seqs))
    assert len(selected_seqs) == len(selected_seq_names)
    return selected_seqs
    
to_write_data = Sequence_selector(result_file_allergens, genome_file_original)

with open(out_file, "w") as out_f:
    for meta in list(to_write_data.keys()):
        protein = meta + to_write_data[meta]
        out_f.write(protein)
        
        
