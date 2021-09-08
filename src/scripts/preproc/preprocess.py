import pickle
import json
from clean import clean
from fix_states import fix_states
from stem import stem

MAX_WORD_LENGTH = 4

with open("scripts/preproc/stopwords.txt") as f:
    stopwords = list([line.rstrip('\n') for line in f])

discs = pickle.load(open('data/speeches_all_merged.pickle', 'rb'))

proc_discs = []
stem_map = {}

size = len(discs)

for i, speech in enumerate(discs):
    current_disc = []

    disc = speech["text"]

    words = disc.split(' ')
    words = [clean(w) for w in words]
    words = fix_states(words)

    for word in words:
        if(
            word and
            word not in stopwords and
            len(word) >= MAX_WORD_LENGTH
        ):
            original_word = word
            word = stem(original_word)

            if(word not in stem_map):
                stem_map[word] = {}

            if(original_word not in stem_map[word]):
                stem_map[word][original_word] = 0

            stem_map[word][original_word] = stem_map[word][original_word] + 1

            current_disc.append(word)


    proc_discs.append(current_disc)

    print('{}/{}\t{:.2f}%'.format(len(proc_discs), size, len(proc_discs)*100/size))

final_discs = []

print('Will unstem.')

for disc in proc_discs:
    current_disc = []

    for word in disc:
        options = stem_map[word]

        max = list(options.items())[0]

        for item in options.items():
            if item[1] > max[1]:
                max = item

        unstemmed_word = max[0]

        current_disc.append(unstemmed_word)

    final_discs.append(current_disc)

with open('data/speeches_preproc.pickle', 'wb') as handle:
    pickle.dump(final_discs, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Inspect
# with open('data/discursos_preproc.txt', 'w+') as handle:
#     handle.write("\n\n\n\n".join(
#         [" ".join(d) for d in final_discs]
#     ))
