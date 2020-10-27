#!/bin/bash
set -e

file=$1

mkdir allergen-hmms
mkdir allergen-hmms/logs
count=0

while read -r line; do
Name=$line
echo "Downloading HMM profile for $Name. Log can be viewed at logs/$Name.log"
pushd allergen-hmms
wget "http://pfam.xfam.org/family/$Name/hmm" -o "logs/$Name.log"
mv hmm $Name
count=$((count+1))
popd
done < $file

echo "$count HMM Profiles downloaded.Exiting."
