from gensim.models.wrappers import LdaMallet
import lda_utils
import file_utils


def run(lda: LdaMallet, out_folder, model_name):
    topic_list = get_topics(lda)
    save_topics(
        topic_list, out_folder, model_name
    )


def get_topics(lda: LdaMallet):
    print("[topics] get_topics()")

    return lda_utils.get_lda_topics_words(lda)


def save_topics(topic_list: [], out_folder: str, model_name: str):
    print("[topics] save_topics()")

    filename = '{}/topic_list.txt'.format(
        out_folder
    )

    with open(filename, 'a') as f:
        file_utils.write_header(f, model_name, close=True)

        f.write('\t'.join([
            'topic',
            'words'
        ]) + '\n')

        for i, words in enumerate(topic_list):
            topic = i

            f.write('{}\t{}\n'.format(
                topic,
                words
            ))

def save_topics_with_samples(lda: LdaMallet, speeches_all_preproc: list, out_folder: str):
    docs_topics = lda_utils.get_docs_topics(lda)

    # most representative topic of each document
    docs_topics = [
        (i, sorted(topics, key=lambda x: x[1], reverse=True)[0])
        for i, topics in enumerate(docs_topics)
    ]

    # item: (i, 28, 0.2)
    docs_topics = [
        (i, topic, weight)
        for (i, (topic, weight)) in docs_topics
    ]

    urls = [
        "https://www25.senado.leg.br/web/atividade/pronunciamentos/-/p/texto/{}".format(speech["id"])
        for speech in speeches_all_preproc
    ]

    filename = '{}/topic_list_samples.txt'.format(
        out_folder
    )

    with open(filename, 'a') as f:

        f.write('\t'.join([
            'topic',
            'words'
        ]) + '\n')

        for topic in range(0, lda.num_topics):
            topic_words = " ".join([
                word
                for (word, _) in lda.show_topic(topic)
            ])

            topic_docs = [
                element
                for element in docs_topics
                if element[1] == topic
            ]

            sorted_topic_docs = sorted(
                topic_docs,
                key=lambda x: x[2], reverse=True
            )

            sorted_topics_docs_slice = sorted_topic_docs[0:5]

            topic_urls = [
                urls[i]
                for (i, topic, weight) in sorted_topics_docs_slice
            ]

            f.write('\n{}\t{}\n'.format(
                topic,
                topic_words
            ))

            for url in topic_urls:
                f.write('- {}\n'.format(
                    url
                ))
