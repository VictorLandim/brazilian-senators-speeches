from random import randint
import os
import shutil
import pickle
import lda_utils
import file_utils
from gensim.models.wrappers import LdaMallet


def run(
        lda: LdaMallet,
        model_name: str,
        texts_raw: [],
        texts_preproc: [],
        out_folder: str,
        sample_ids: [],
):
    doc_samples = get_samples(
        lda, [], model_name, texts_raw, texts_preproc, sample_ids
    )

    save_samples(doc_samples, out_folder, model_name)


def get_samples(
    lda: LdaMallet,
    corpus: [],
    model_name: str,
    texts_raw: [],
    texts_preproc: [],
    sample_ids: [] = [],
    preproc=False,
):
    """
    Builds a structure of `n` random documents and their top topics.
    """
    print("[sample] get_samples()")

    size = len(texts_raw)

    if len(sample_ids) == 0:
        num_samples = 5
        sample_ids = [randint(0, size)
                      for _ in range(num_samples)]

    docs_topics = lda_utils.get_docs_topics(lda)

    docs_topics = [
        sorted(
            doc,
            key=lambda x: x[1],
            reverse=True
        )
        for doc in docs_topics
    ]

    samples_list = [
        {
            "id": i,
            "topics": [
                (
                    topic,
                    "{}%".format(
                        format(weight*100, ".2f")
                    ),
                    lda_utils.get_lda_topics_words(lda)[topic]
                )
                for (topic, weight) in docs_topics[i]
            ],
            "text_raw": texts_raw[i],
            "text_preproc": " ".join(texts_preproc[i])
        }
        for i in sample_ids
    ]

    return samples_list


def save_samples(sample_list: [], out_folder: str, model_name: str):
    """
    Saves sample structure to file.
    """

    print("[sample] save_samples()")

    folder = "{}/samples".format(out_folder)
    file_utils.recreate_folder(folder)

    for sample_item in sample_list:
        id = sample_item["id"]
        topics = sample_item["topics"]
        text_preproc = sample_item["text_preproc"]

        disc_data = sample_item["text_raw"]

        text_raw = disc_data["Conteudo"]
        senator = disc_data["IdentificacaoParlamentar"]["NomeParlamentar"]
        date = disc_data["IdentificacaoPronunciamento"]["DataPronunciamento"]
        party = disc_data["IdentificacaoPronunciamento"]["SiglaPartidoParlamentarNaData"]
        state = disc_data["IdentificacaoPronunciamento"]["UfParlamentarNaData"]
        url = disc_data["IdentificacaoPronunciamento"]["UrlTexto"]
        code = disc_data["IdentificacaoPronunciamento"]["CodigoPronunciamento"]

        filename = '{}/{}.txt'.format(
            folder, id
        )

        with open(filename, 'a', encoding="utf-8") as f:
            file_utils.write_header(f, model_name, close=False)
            f.write("\nCodigoPronunciamento:\t\t{}".format(
                code
            ))
            f.write("\nUrlTexto:\t\t\t{}".format(
                url
            ))
            f.write("\nDataPronunciamento:\t\t{}".format(
                date
            ))
            f.write("\nNomeParlamentar:\t\t{}".format(
                senator
            ))
            f.write("\nSiglaPartidoParlamentarNaData:\t{}".format(
                party
            ))
            f.write("\nUfParlamentarNaData:\t\t{}\n".format(
                state
            ))
            file_utils.write_separator(f)

            f.write("\nMain topics:\n\n")

            f.write('\t'.join([
                'topic',
                'weight',
                'words'
            ]) + '\n')

            for (topic, weight, words) in topics:
                f.write('{}\t{}\t{}\n'.format(
                    topic,
                    weight,
                    words
                ))

            file_utils.write_separator(f)
            f.write("\nOriginal document:\n\n")
            f.write(text_raw)

            f.write("\n")
            file_utils.write_separator(f)
            f.write("\nPreprocessed document:\n\n")
            f.write(text_preproc)
