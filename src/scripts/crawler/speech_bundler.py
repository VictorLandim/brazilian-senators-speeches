import json
import pickle
import glob
import os

def bundle(folder: str):
    all_speeches = []

    for filename in glob.iglob('data/speeches_raw_{}/*.json'.format(folder), recursive=False):
        if not os.path.isfile(filename):
            continue

        speech = json.load(open(filename, "r"))
        all_speeches.append(speech)

    print("Count: {}".format(len(all_speeches)))

    with open('speeches_all_{}.pickle'.format(folder), 'wb') as handle:
        pickle.dump(all_speeches, handle, protocol=pickle.HIGHEST_PROTOCOL)

bundle("date")
bundle("legislature")