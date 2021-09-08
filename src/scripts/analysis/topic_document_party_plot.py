import pickle
from gensim.models.wrappers import LdaMallet
from gensim.corpora.dictionary import Dictionary
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from party import sort_documents_by_party, clean_party
sns.set()

lda = LdaMallet.load("data/models/lda_model_50_stem_it_2000/model")

texts_raw = pickle.load(open("data/discursos_raw_all.pickle", "rb"))

doc_topics = [
    x
    for x in lda.read_doctopics(lda.fdoctopics(), eps=0.01, renorm=True)
]

docs_party = sort_documents_by_party(texts_raw)

sorted_doc_topics = [
    sorted(x, key=lambda x: x[1], reverse=True)[0]
    for x in doc_topics
]

topic_map = {}

for party, _ in docs_party.items():
    for doc in docs_party[party]:
        topic, weight = sorted_doc_topics[doc]

        item = (doc, weight, party)

        if topic in topic_map:
            topic_map[topic].append(item)
        else:
            topic_map[topic] = [item]

    LIMIT = 20
    for key, _ in topic_map.items():
        topic_map[key] = sorted(
            topic_map[key], key=lambda x: x[1], reverse=True)[0:LIMIT]

df = pd.DataFrame()

current_topic = 30

for i, topic in enumerate(topic_map[current_topic]):
    doc, weight, party = topic
    df = df.append(
        pd.Series([doc, party, round(weight, 2)]), ignore_index=True)

df.columns = ['Document', 'Party', 'Weight']

ax = df["Party"].value_counts().plot(kind='bar')
ax.set_title("Topic {}".format(current_topic))

outdir = "results/party_topic_plot"

fig = ax.get_figure()
fig.savefig("{}/topic_{}.png".format(outdir, current_topic))
