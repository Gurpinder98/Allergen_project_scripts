import os
import sys

GENOME_FOLDER=sys.argv[1]
PFAM_FOLDER=sys.argv[2]

CURRENT_DIR = os.getcwd()

Genome_list = os.listdir(GENOME_FOLDER)
Genome_list_extended = [CURRENT_DIR+"/"+GENOME_FOLDER+"/"+Genome_list[i] for i in range(len(Genome_list))]

pfam_id_list = os.listdir(PFAM_FOLDER)
pfam_id_list_extended = [CURRENT_DIR+"/"+PFAM_FOLDER+"/"+pfam_id_list[i] for i in range(len(pfam_id_list))]


with open("genomes_list.txt", "w") as out_f:
    out_f.write('\n'.join(Genome_list_extended)+'\n')

with open("pfam_list.txt","w") as out_f:
    out_f.write("\n".join(pfam_id_list_extended)+'\n')



