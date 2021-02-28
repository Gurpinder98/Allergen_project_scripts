import os

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
                accession = line.split(" ")[0][1:-1]
                seq = ""
            else:
                seq = seq + line
            seqs[accession] = seq
    return seqs

in_file_name = input("Enter file name: ")
out_folder_name = input("Enter folder name: ")
os.mkdir(out_folder_name)

all_seqs = reader(in_file_name)
count = 0
for accession in list(all_seqs.keys()):
    out_file_name = out_folder_name + "\\" + accession
    with open(out_file_name, "w") as out_f:
        out_f.write(">"+accession+"\n"+all_seqs[accession])
        count += 1
    print("{} done.".format(accession))
print("{} files writen in {}".format(str(count), out_folder_name))

    