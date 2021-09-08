import json
import pickle
import glob
import os
import pandas as pd

all_speeches = []

for filename in glob.iglob('data/speeches_raw/*.json', recursive=False):
    if not os.path.isfile(filename):
        continue

    speech = json.load(open(filename, "r", encoding="utf-8"))

    all_speeches.append(speech)

print("Count: {}".format(len(all_speeches)))

df_speeches = [
  {
    "id": x["@id"],
    "date": x["Data"],
    "type": "{} - {}".format(x["TipoUsoPalavra"]["Sigla"], x["TipoUsoPalavra"]["Descricao"]),
    "session": "{} - {}".format(x["Sessao"]["TipoSessao"], x["Sessao"]["DescricaoSessao"])
  }
  for x in all_speeches
]

pd.set_option('display.max_rows', None)
df = pd.DataFrame(df_speeches)
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year

print('year')
print(df[['year', 'id']].groupby('year').count())

print('Disc type')
print(df[['type', 'id']].groupby('type').count())

print('Session type')
print(df[['session', 'id']].groupby('session').count())