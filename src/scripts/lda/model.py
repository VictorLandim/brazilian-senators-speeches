from gensim.models.wrappers.ldamallet import malletmodel2ldamodel
from gensim.corpora.dictionary import Dictionary
from gensim.models.wrappers import LdaMallet
from gensim.models import LdaModel
import time
import os


def create_model(
    texts,
    corpus,
    dictionary,
    num_topics,
    prefix,
    workers=4,
    topic_threshold=0.0,
    iterations=1000,
    optimize_interval=0,
) -> LdaMallet:
    """
    `texts`: array of arrays of tokens
    `prefix`: model data folder
    """
    mallet_path = "lib/mallet-2.0.8/bin/mallet"

    if prefix and not os.path.exists(prefix):
        os.makedirs(prefix)

    start_time = time.time()

    lda = LdaMallet(mallet_path,
                    corpus=corpus,
                    id2word=dictionary,
                    num_topics=num_topics,
                    iterations=iterations,
                    topic_threshold=topic_threshold,
                    prefix=prefix,
                    optimize_interval=optimize_interval,
                    # workers=workers,
                    )

    elapsed_time = time.time() - start_time

    print(time.strftime("Lda model for num_topics = {} created, took %H:%M:%S:%m".format(
        num_topics), time.gmtime(elapsed_time)))

    return lda
