# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 12:16:12 2021

@author: Gurpinder
"""
from Bio import SeqIO
import pandas as pd
import numpy as np
import biovec
pv = biovec.models.load_protvec("/home/gurpinder/swissprot-reviewed-protvec.model")

#parse the sequences and store in a pandas df
positive_ex = SeqIO.parse('positive.fasta', format='fasta')
positives = []
for sequence in positive_ex:
    positives.append([sequence.id, str(sequence.seq), 0])

negative_ex = SeqIO.parse('negative.fasta', format='fasta')
negatives = []
for sequence in negative_ex:
    negatives.append([sequence.id, str(sequence.seq), 1])


positive_df = pd.DataFrame(positives, columns=(['Seq ID', 'Seq', 'Class']))
negative_df = pd.DataFrame(negatives, columns=(['Seq ID', 'Seq', 'Class']))

total_data = pd.concat([positive_df, negative_df], axis=0)
# add another column in pandas df to contain 100x3 vector from biovec

all_seqs = total_data.Seq.to_list()
all_seq_vectors = []

for seq in all_seqs:
    temp_arr = pv.to_vecs(seq)
    all_seq_vectors.append([list(temp_arr[0])+list(temp_arr[1])+list(temp_arr[2])])
    #all_seq_vectors.append(['test','test'])
total_data['Vectors'] = all_seq_vectors

total_data.to_csv("test.csv", sep=",", index=False)
