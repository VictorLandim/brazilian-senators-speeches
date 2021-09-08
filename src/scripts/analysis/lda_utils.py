import pickle
from gensim.models.wrappers import LdaMallet


def get_docs_topics(lda: LdaMallet, topic_threshold=0.01):
    """
    Remove topics with small contribution, default = 1%.
    Read topics from model_data/doctopics.txt
    """

    lda_doc_topics = lda.read_doctopics(
        lda.fdoctopics(), eps=topic_threshold, renorm=True
    )

    doc_topics = [
        x
        for x in lda_doc_topics
    ]

    return doc_topics


def get_lda_topics_words(lda: LdaMallet):
    """
    For a given index, return a word list string of the topic.
    """

    lda_topics = lda.show_topics(
        formatted=False, num_words=10, num_topics=lda.num_topics
    )

    return [
        ", ".join([
            word
            for (word, prob) in words
        ])
        for (topic, words) in lda_topics
    ]


def get_corpus():
    return pickle.load(open("data/corpus.pickle", "rb"))


def get_texts_raw():
    return pickle.load(open("data/discursos_raw_all.pickle", "rb"))


def get_texts_preproc():
    return pickle.load(open("data/discursos_preproc.pickle", "rb"))
