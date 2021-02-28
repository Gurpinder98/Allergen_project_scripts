# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 17:29:37 2020

@author: Gurpinder
"""
from Bio import Entrez
from urllib.error import HTTPError
import time
import argparse


def parser_func():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-email', '-e', type=str, required = True,
                        help = 'Email required to fetch data from NCBI')
    parser.add_argument('-input', '-i', type=str, required = True,
                        help = 'Input file (containing accession numbers)')
    parser.add_argument('-output', '-o', type=str, required = True,
                        help = 'Output file')
    parser.add_argument('-database', '-db', type=str, required = True,
                        help = 'Database')
    return parser.parse_args()


def file_reader(file):
    """
    Reads the input file with accessions into a list.
    """
    accessions = []
    try:
        with open(file, "r") as in_f:
            lines = in_f.readlines()
        accessions = [line.strip() for line in lines]
    except FileNotFoundError:
        print("Input file not found.")
        
    return accessions

args = parser_func()

Entrez.email = args.email
output_file = args.output
input_file = args.input
dataB = args.database
accessions = file_reader(input_file) #read the file

to_write = ''
for accession in accessions: 
    print("Downloading {}".format(accession))        
    try:
        FASTA  = Entrez.efetch(db=dataB, id=accession, rettype="fasta", retmode="text")
        to_write_temp = FASTA.read()
        assert len(to_write_temp) > 0
        to_write = to_write + to_write_temp[:-1]
    except HTTPError:
        print("{} not available".format(accession))
        continue
        
with open(output_file, "w") as out_f:  
  out_f.write(to_write)

    
    
    