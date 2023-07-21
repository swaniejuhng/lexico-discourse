import numpy as np
import pickle

with open("glove.twitter.27B.25d.txt") as f:
    lines = f.readlines()
    word_embeds = dict([(l.split(maxsplit=1)[0], np.array([float(n) for n in l])) for l in lines])

with open("glove_25.dict", "wb") as f:
    pickle.dump(word_embeds, f)