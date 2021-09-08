import pickle
from gensim.models.wrappers import LdaMallet

def run(model_name: str, corpus: list) -> None:
  model_path = "data/models/{}/model".format(model_name)
  lda = LdaMallet.load(model_path)
  docs_topics = lda[corpus]
  with open('data/docs_topics_{}.pickle'.format(model_name), 'wb') as handle:
    pickle.dump(docs_topics, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    model_name = "50_it_10000"
    corpus = pickle.load(open("data/corpus.pickle","rb"))
    run(model_name,corpus)
