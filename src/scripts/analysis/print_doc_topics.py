import pickle
from gensim.models.wrappers import LdaMallet
import lda_utils
import os

def print_doc_topics(id: str, model_name: str, speeches: list) -> None:
  model_path = "data/models_new/{}/model".format(model_name)

  lda = LdaMallet.load(model_path)
  lda.mallet_path = "lib\\mallet-2.0.8\\bin\\mallet"
  os.environ['MALLET_HOME'] = 'X:\\Programs\\Java\\mallet\\mallet-2.0.8'

  docs_topics = pickle.load(open("data/docs_topics_good_{}.pickle".format(model_name), "rb"))
  topics_words = lda_utils.get_lda_topics_words(lda)

  speech_index = [
    i
    for i, speech in enumerate(speeches)
    if speech['id'] == id
  ][0]

  doc_topics = docs_topics[speech_index]

  doc_topics_words = [
    (topic, weight, topics_words[topic])
    for (topic, weight) in doc_topics
  ]

  sorted_doc_topics = sorted(doc_topics_words, key=lambda x: x[1], reverse=True)
  print("{}\t{}\t{}\t".format(
    "topic",
    "weight",
    "words",
  ))
  for (topic, weight, words) in sorted_doc_topics:
    print("{}\t{}\t{}\t".format(
      topic, "{}%".format(round(weight*100, 2)), words
    ))

if __name__ == '__main__':
  speech_id = '370609'
  model_name = "65_it_10000"
  speeches = pickle.load(open("data/speeches_all_preproc_filtered.pickle", "rb"))

  print_doc_topics(speech_id, model_name, speeches)