from gensim.models.wrappers import LdaMallet
from gensim.models import CoherenceModel
import sys
import os
sys.path.append('scripts/analysis')
from analysis import file_utils  # nopep8


def write_header(filename):
    with open(filename, "a") as f:
        file_utils.write_header(f, "--")

        f.write("Coherence values:\n\n")

        f.write("{: <15} {: <15} {: <15} {: <15}\n".format(
            "num_topics",
            "iterations",
            "opt_interval",
            "coherence",
        ))


def write_values_to_file(filename, values):
    with open(filename, "a") as f:
        num_t, it, opt_i, value = values

        f.write("{: <15} {: <15} {: <15} {: <15}\n".format(
            num_t,
            it,
            opt_i,
            value
        ))


def create_coherence_model(lda: LdaMallet, dictionary, texts):
    coherence_model = CoherenceModel(
        model=lda,
        texts=texts,
        dictionary=dictionary,
        coherence='c_v'
    )

    result_data = (
        lda.num_topics,
        lda.iterations,
        lda.optimize_interval,
        coherence_model.get_coherence()
    )

    return result_data
