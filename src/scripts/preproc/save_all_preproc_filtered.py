import pickle
from datetime import datetime
import pandas as pd

def filter_speeches(outdir: str) -> None:
  ALLOWED_SPEECH_TYPE = "DIS"
  MIN_PREPROC_LENGTH = 20
  MIN_YEAR = 1995
  MAX_YEAR = 2020

  speeches_preproc  = pickle.load(open('data/speeches_preproc.pickle', 'rb'))
  speeches_all      = pickle.load(open('data/speeches_all_merged.pickle', 'rb'))

  speeches_filtered = []

  print("Speeches all size: {}".format(len(speeches_all)))
  print("Speeches preproc size: {}".format(len(speeches_preproc)))

  for i, speech in enumerate(speeches_all):
    speech_type    = speech["speech_type"]
    preproc_length = len(speeches_preproc[i])
    speech_year    = datetime.strptime(speech["date"], "%Y-%m-%d").year
    is_year_valid  = speech_year >= MIN_YEAR and speech_year <= MAX_YEAR

    if (speech_type == ALLOWED_SPEECH_TYPE and
        preproc_length >= MIN_PREPROC_LENGTH and
        is_year_valid):
      current_speech = speech
      current_speech["text_preproc"] = speeches_preproc[i]
      speeches_filtered.append(current_speech)

  print("Filtered speeches size: {}".format(len(speeches_filtered)))
  print("Year count:")
  df = pd.DataFrame([datetime.strptime(s["date"], "%Y-%m-%d").year for s in speeches_filtered])
  print(df.groupby(0).size())

  with open('{}/speeches_all_preproc_filtered.pickle'.format(outdir), 'wb') as handle:
    pickle.dump(speeches_filtered, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
  outdir = "data"
  filter_speeches(outdir)