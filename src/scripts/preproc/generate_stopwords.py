import csv
import pickle
import nltk
from spacy.lang.pt import STOP_WORDS
from clean import clean

stopwords = []

with open('scripts/preproc/stopwords_from_topics.txt') as f:
    topic_words = f.read().splitlines()

with open('scripts/preproc/custom_stopwords.txt') as f:
    custom_words = f.read().splitlines()

# spacy
spacy_words = list(STOP_WORDS)

# nltk
nltk_words = nltk.corpus.stopwords.words('portuguese')

name_words = []
party_words = []
state_words = []

# also remove party names and state abbreviations
discs = pickle.load(open('data/discursos_raw_all.pickle', 'rb'))

for disc in discs:
    names = disc['IdentificacaoParlamentar']['NomeCompletoParlamentar'].split(
        ' ')
    name_words = list(set(name_words + names))

    if 'SiglaPartidoParlamentarNaData' in disc['IdentificacaoPronunciamento']:
        party = disc['IdentificacaoPronunciamento']['SiglaPartidoParlamentarNaData']
        party_words = list(set(party_words + [party]))

    if 'UfParlamentarNaData' in disc['IdentificacaoPronunciamento']:
        state = disc['IdentificacaoPronunciamento']['UfParlamentarNaData']
        state_words = list(set(state_words + [state]))

stopwords = list(set(
    topic_words +
    custom_words +

    spacy_words +
    nltk_words +

    name_words +
    party_words +
    state_words
))

stopwords = [clean(word) for word in stopwords]

stopwords = list(set(stopwords))

# keep only words with 4 or more characters
stopwords = [w for w in stopwords if len(w) >= 4]

# sort
stopwords = sorted(stopwords)

with open('scripts/preproc/stopwords.txt', "w+") as f:
    f.write('\n'.join(stopwords))
