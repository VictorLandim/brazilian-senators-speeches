from model import create_model
import pickle

speeches_all = pickle.load(open('data/speeches_all_preproc_filtered.pickle', 'rb'))
texts = [s["text_preproc"] for s in speeches_all]
corpus = pickle.load(open('data/corpus_final.pickle', 'rb'))
dictionary = pickle.load(open('data/dictionary_final.pickle', 'rb'))

lda_params = [
    {
        "num_topics": 65,
        "iterations": 10000,
    },
]

for param in lda_params:
    folder = "data/models/{}_it_{}".format(
        param["num_topics"],
        param["iterations"],
    )

    lda = create_model(
        texts,
        corpus,
        dictionary,
        param["num_topics"],
        prefix=folder,
        iterations=param["iterations"],
        topic_threshold=0
    )

    lda.save("{}/model".format(folder))

print('{} models created.'.format(
    len(lda_params)
))
