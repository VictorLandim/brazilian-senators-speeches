from gensim.models import CoherenceModel
from gensim.models.wrappers import LdaMallet
import pickle
import sys
import os
sys.path.append('scripts/analysis')
from analysis import file_utils  # nopep8
import coherence_utils  # nopep8
from model import create_model  # nopep8


def create_all_coherence_new_models(
        out_file: str,
        dictionary,
        corpus,
        texts, start, limit, step
):

    for num_topics in range(start, limit, step):
        lda = create_model(
            texts=texts,
            num_topics=num_topics,
            prefix="/tmp",
            iterations=1000,
            topic_threshold=0,
            corpus=corpus,
            dictionary=dictionary,
        )

        print("[coherence] model created for n={}".format(
            num_topics))

        result_data = coherence_utils.create_coherence_model(
            lda, dictionary, texts
        )

        coherence_utils.write_values_to_file(out_file, result_data)

        print("[coherence] coherence created for n={}, opt_int={}".format(
            num_topics))


if __name__ == "__main__":
    out_folder = "results/coherence"
    out_file = "{}/coherence_values_new_model.txt".format(out_folder)

    file_utils.recreate_folder(out_folder)
    coherence_utils.write_header(out_file)

    dictionary = pickle.load(open("data/dictionary.pickle", "rb"))
    corpus = pickle.load(open("data/corpus.pickle", "rb"))
    texts = [speech['text_preproc'] for speech in pickle.load(
        open("data/speeches_all_preproc_filtered.pickle", "rb"))]

    print("[main] dict, corpus, texts fetched")

    start = 50
    step = 50
    limit = 1000

    create_all_coherence_new_models(
        out_file, dictionary, corpus, texts,
        start, limit, step,
    )

    print("[coherence] done")
