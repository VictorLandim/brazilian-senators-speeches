import pickle
from clean import clean

MAX_WORD_LENGTH = 3

stopwords = pickle.load(open('stopwords.pickle', 'rb'))

discs = pickle.load(open('../../data/discursos_texts.pickle', 'rb'))

all = []

for disc in discs[0:10000]:
    current_disc = []

    words = disc.split(' ')

    for word in words:
        word = clean(word)

        if not word:
            continue

        if word not in stopwords and len(word) >= MAX_WORD_LENGTH:
            current_disc.append(word)

    selected_words = [x for x in current_disc if len(x) == MAX_WORD_LENGTH]

    all = all + selected_words

all = set(all)

with open('3_letter_words.txt', 'w+') as f:
    f.write('\n'.join(all))
