# import pandas as pd
from sentence_transformers import SentenceTransformer
import csv
# from collections import defaultdict
import numpy as np
from tqdm import tqdm

# model_path = "/data1/sjuhng/phrase-bert-model/pooled_context_para_triples_p=0.8"
# model = SentenceTransformer(model_path)
model = SentenceTransformer('all-MiniLM-L6-v2')

file_name = sys.argv[1]
output_name = file_name[:-19] + ".sbert.csv"

with open(file_name, "r") as r:
    reader = csv.reader(r)
    with open(output_name, "w") as w:
        writer = csv.writer(w)
        id = 1
        for i, sentences in enumerate(reader):
            if i % 10000 == 0:
                print(i)
            sentence_embeddings = model.encode(sentences)
            sentence_embeddings = np.mean(sentence_embeddings, axis=0)
            for j in range(384):
                group_norm = sentence_embeddings[j]
                writer.writerow([id, i+1, "sbert_"+str(j), round(group_norm), group_norm])
                id += 1