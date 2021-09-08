import pickle

def normalize_single_doc_topics(doc_topics: list) -> None:
  total = sum([weight for _, weight in doc_topics])

  normalized = [(topic, weight / total) for topic, weight in doc_topics]

  return normalized


def run(model_name):
  docs_topics = pickle.load(open("data/docs_topics_{}.pickle".format(model_name), "rb"))

  with open("data/bad_topics_{}.txt".format(model_name)) as f:
    bad_topics = [int(line.strip()) for line in f.readlines()]

    new_docs_topics = []

    for doc in docs_topics:
      new_doc_topics = list(filter(
        lambda x: x[0] not in bad_topics,
        doc))

      normalized_doc_topics = normalize_single_doc_topics(new_doc_topics)

      new_docs_topics.append(normalized_doc_topics)

    with open('data/docs_topics_good_{}.pickle'.format(model_name), 'wb') as handle:
      pickle.dump(new_docs_topics, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
  model_name = "40_it_10000"
  run(model_name)