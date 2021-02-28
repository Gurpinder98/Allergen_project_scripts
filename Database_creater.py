# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 17:29:37 2020

@author: Gurpinder
"""
from Bio import Entrez
from urllib.error import HTTPError
import time
import sys
import argparse


def file_reader(file):
    accessions = []
    with open(file, "r") as in_f:
        lines = in_f.readlines()
    accessions = [line.strip() for line in lines]
    return accessions

parser = argparse.ArgumentParser()
parser.add_argument('--email', '-e', type=str,
                    help = 'Email required to fetch data from NCBI')
parser.add_argument('--input', '-i', type=str,
                    help = 'Input file containing accession numbers')
parser.add_argument('--output', '-o', type=str,
                    help = 'Output file')

args = parser.parse_args()

# Add Email here!!
Entrez.email = args.email
output_file = args.output
input_file = args.input

accessions = file_reader(input_file)
to_write = ''
for accession in accessions: 
    print("Downloading {}".format(accession))        
    try:
        FASTA  = Entrez.efetch(db="protein", id=accession, rettype="fasta", retmode="text")
        to_write_temp = FASTA.read()
        assert len(to_write_temp) > 0
        to_write = to_write + to_write_temp[:-1]
    except HTTPError:
        print("{} not available".format(accession))
        continue
        
with open(output_file, "w") as out_f:  
  out_f.write(to_write)

    
    
    