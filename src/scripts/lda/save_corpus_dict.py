import pickle
from gensim.models.wrappers import LdaMallet
from gensim.corpora.dictionary import Dictionary
import pandas as pd
import numpy as np

speeches_all = pickle.load(open('data/speeches_all_preproc_filtered.pickle', 'rb'))
texts = [speech["text_preproc"] for speech in speeches_all]

dictionary = Dictionary(texts)
corpus = [dictionary.doc2bow(t) for t in texts]

dict_corpus = {}

for i in range(len(corpus)):
    for idx, freq in corpus[i]:
        if dictionary[idx] in dict_corpus:
            dict_corpus[dictionary[idx]] += freq
        else:
            dict_corpus[dictionary[idx]] = freq

dict_df = pd.DataFrame.from_dict(dict_corpus, orient='index', columns=['freq'])
print(dict_df.sort_values('freq', ascending=False).head(20))

# this should be determined exploratorily
MAX_FREQUENCY = 157623
extension = dict_df[dict_df.freq > MAX_FREQUENCY].index.tolist()

print("Removed words: {}".format(extension))

ids = [dictionary.token2id[extension[i]] for i in range(len(extension))]
dictionary.filter_tokens(bad_ids=ids)

print("Dict size before extreme filtering: {}".format(len(dictionary)))

# from izumi and davi
no_below = int(len(texts) * 0.5 / 100)

dictionary.filter_extremes(
    no_below=no_below, # 0.5%
    no_above=90 # 90%
)

print("Dict size after extreme filtering: {}".format(len(dictionary)))

# recreate corpus
corpus = [dictionary.doc2bow(t) for t in texts]

with open('data/dictionary.pickle', 'wb') as handle:
    pickle.dump(dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('data/corpus.pickle', 'wb') as handle:
    pickle.dump(corpus, handle, protocol=pickle.HIGHEST_PROTOCOL)
