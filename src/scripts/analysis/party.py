import os
import shutil
import time
import pickle
from datetime import date
from gensim.models.wrappers import LdaMallet
import lda_utils
import file_utils


def run(lda: LdaMallet, out_folder: str, model_name: str, texts_raw: []) -> None:
    disc_by_party = sort_documents_by_party(texts_raw, party_threshold=750)
    topics_by_party = get_topics_by_party(
        lda, disc_by_party
    )
    save_topics_by_party(disc_by_party, topics_by_party,
                         out_folder, model_name)


def clean_party(party):
    # normalize party names
    party_alias = {
        "DEM":              "PFL",
        "DEMOCRATAS":       "PFL",
        "PL":               "PR",
        "PRONA":            "PR",
        "PDC":              "PP",
        "PST":              "PP",
        "PTR":              "PP",
        "PRB":              "PP",
        "PPR":              "PP",
        "PPB":              "PP",
        "PROGRESSISTAS":    "PP",
        "PC DO B":          "PCdoB",
        "PODEMOS":          "PODE",
        "S/PARTIDO":        "S-PARTIDO",
        "S/Partido":        "S-PARTIDO",
    }

    if party in party_alias:
        return party_alias[party]

    return party


def sort_documents_by_party(texts_raw: [], party_threshold=750):
    empty_ids = []  # invalid docs

    # = {
    #  "PT":   [1, 4, 10, 3434],
    #  "PMDB": [2, 11, 534, 99]
    #   ...
    # }
    disc_by_party = {}

    for i, disc in enumerate(texts_raw):
        d = disc["IdentificacaoPronunciamento"]

        if 'SiglaPartidoParlamentarNaData' not in d:
            empty_ids.append(i)

        else:
            party = d["SiglaPartidoParlamentarNaData"].strip()

            party = clean_party(party)

            if party not in disc_by_party:
                disc_by_party[party] = [i]
            else:
                disc_by_party[party].append(i)

    # only process parties with `party_threshold` docs or more
    disc_by_party_filtered = {
        k: v for k, v in disc_by_party.items() if len(v) >= party_threshold}

    return disc_by_party_filtered


def get_topics_by_party(lda: LdaMallet, disc_by_party):
    print("[party] get_topics_by_party()")

    topics = lda_utils.get_lda_topics_words(lda)
    doc_topics = lda_utils.get_docs_topics(lda, topic_threshold=0.01)

    topics_by_party = {}

    for current_party in disc_by_party:
        party_discs = disc_by_party[current_party]

        current_party_len = len(party_discs)

        topic_weight_map = {}
        topic_count_map = {}

        for i in party_discs:
            current_doc_topics = doc_topics[i]

            #  sorted_doc = sorted(
            # lda[corpus][i], key=lambda x: (x[1]), reverse=True)[0:10]
            # lda[corpus][i], key=lambda x: (x[1]), reverse=True)

            for topic, weight in current_doc_topics:

                # weight
                if topic not in topic_weight_map:
                    topic_weight_map[topic] = weight
                else:
                    topic_weight_map[topic] += weight

                # count
                if topic not in topic_count_map:
                    topic_count_map[topic] = 1
                else:
                    topic_count_map[topic] += 1

        sorted_topics_map = sorted(
            topic_weight_map.items(), key=lambda x: x[1], reverse=True
        )

        # so that values go from 0 to 100
        normalizing_factor = current_party_len / 100

        sorted_topics_map = [
            (
                x,
                "{}%".format(
                    format(y/normalizing_factor, ".6f")
                ),
                "{}/{} ({}%)".format(
                    format(topic_count_map[x], "0{}d".format(
                        len(str(current_party_len))
                    )),
                    current_party_len,
                    format(topic_count_map[x]*100/current_party_len, ".2f")
                ),
                topics[x]
            )
            for (x, y) in sorted_topics_map
        ]

        topics_by_party[current_party] = sorted_topics_map

    return topics_by_party


def save_topics_by_party(disc_by_party, topics_by_party, out_folder, model_name):
    print("[party] save_topics_by_party()")

    folder = "{}/party".format(out_folder)
    file_utils.recreate_folder(folder)

    for current_party in topics_by_party:
        current_party_topics = topics_by_party[current_party]

        filename = '{}/{}.txt'.format(
            folder, current_party
        )

        with open(filename, 'a') as f:
            file_utils.write_header(f, model_name, close=False)

            f.write("\nParty:\t\t\t{}".format(
                current_party
            ))
            f.write("\nN# of documents:\t{}\n".format(
                len(disc_by_party[current_party])
            ))

            file_utils.write_separator(f)
            f.write("\n")

            f.write('\t'.join([
                'topic',
                'weight %',
                'frequency\t',
                'words'
            ]) + '\n')

            for (topic, weight, freq, words) in current_party_topics:
                f.write('{}\t{}\t{}\t{}\n'.format(
                    topic, weight, freq, words
                ))
