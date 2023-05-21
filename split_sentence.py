from sentence_splitter import SentenceSplitter, split_text_into_sentences
import csv
import sys
from tqdm import tqdm
#
# Object interface
#
infile = sys.argv[1]
outfile = infile[:-4]+".sentence_split.csv"

with open(infile, "r") as r:
    lines = r.readlines()
splitter = SentenceSplitter(language='en')
with open(outfile, "w") as w:
    writer = csv.writer(w)
    for line in tqdm(lines):
        writer.writerow(splitter.split(text=line))