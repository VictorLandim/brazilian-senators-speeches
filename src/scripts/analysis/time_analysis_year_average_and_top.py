# pip install gensim==3.8.1 --user

import pickle
from gensim.models.wrappers import LdaMallet
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
import os
import shutil
import datetime
from topics import run as save_topic_list, save_topics_with_samples


def display_single_lda_topic(lda: LdaMallet, topic: int):
  topic = ", ".join([x[0] for x in lda.show_topic(topic)])sorted(topics_map.items(), key=lambda x: x[1], reverse=True)/plot

  return topic

def display_lda_topics(lda: LdaMallet):
  num_topics = lda.num_topics
  topics = [
    (i,
        ", ".join([x[0] for x in lda.show_topic(i)])
    )
    for i in range(num_topics)
  ]
  return topics


def save_frequency_all_plot(df: pd.DataFrame, title: str, filename: str) -> None:
  plot = df.plot(x='year', y='count', marker='o', linestyle='-', grid=True, figsize=(13,7), legend=False)

  plot.set(title=title, xlabel="Ano")

  xticks = df['year'].to_list()
  plot.set_xticks(xticks)

  plot.xaxis.set_tick_params(rotation=45)
  plot.patch.set_facecolor('white')

  fig = plot.get_figure()
  fig.savefig(filename, format='png', dpi=200)
  fig.clf()


def save_frequency_plot(speeches_year_topic_percentage: pd.DataFrame, top_speeches_for_topic_df: pd.DataFrame, title: str, filename: str) -> None:
  df = speeches_year_topic_percentage.copy()
  df['top_speech_percentage'] = top_speeches_for_topic_df['top_speech_percentage']

  # 15. 8
  plot = df.plot(x='year', y=['percentage', 'top_speech_percentage'], marker='o', linestyle='-', grid=True, figsize=(13,7), label=[
    '% da contribuição média do tópico nos discursos do ano',
    '% de discursos onde tópico é dominante no ano'
  ])

  plot.set_title(title)
  plot.set(title=title, xlabel="Ano")

  xticks = df['year'].to_list()
  plot.set_xticks(xticks)

  plot.legend(loc="upper right")
  # plot.set_ylim(0.0, 12.0)
  # plot.set_yticks(range(0, 12 + 1))
  plot.yaxis.set_major_formatter(mtick.FuncFormatter('{}%'.format))

  plot.xaxis.set_tick_params(rotation=45)
  plot.patch.set_facecolor('white')

  fig = plot.get_figure()

  fig.savefig(filename, format='png', dpi=200)
  fig.clf()


def generate_topic_plot(
  speeches_all_preproc,
  top_speeches_for_topic_df,
  topic_speeches_df,
  speeches_year_count_df,
  topic: int,
  outdir: str,
  lda: LdaMallet,
):
  speeches_year_weight_sum = pd.DataFrame(columns={'year': int(), 'weight_sum': float()})

  year_range = range(1995, 2019 + 1)
  for i, current_year in enumerate(year_range):
    speeches_for_year_topic_df = topic_speeches_df[
        topic_speeches_df['year'] == current_year
    ]
    speeches_year_weight_sum.loc[i] = {
        "year": current_year,
        "weight_sum": speeches_for_year_topic_df[['weight']].sum()['weight']
    }

  speeches_year_topic_percentage = speeches_year_count_df.copy()
  speeches_year_topic_percentage.drop('count', axis=1, inplace=True)
  speeches_year_topic_percentage['percentage'] = (speeches_year_weight_sum['weight_sum'] / speeches_year_count_df['count']) * 100

  save_frequency_plot(
    speeches_year_topic_percentage=speeches_year_topic_percentage,
    top_speeches_for_topic_df=top_speeches_for_topic_df,
    title="Tópico {}\n{}".format(topic, display_single_lda_topic(lda, topic)),
    filename="{}/topic_{}.png".format(outdir, topic)
  )

def get_bad_topics(model_name: str) -> list:
    f = open("data/bad_topics_{}.txt".format(model_name))
    bad_topics = [int(line.strip()) for line in f.readlines()]
    f.close()

    return bad_topics

def build_speeches_year_count_df(all_speeches: list) -> pd.DataFrame:
  speeches_date_df = pd.DataFrame([(i, s['date']) for i, s in enumerate(all_speeches)], columns=["i", "date"])
  speeches_date_df['date'] = pd.to_datetime(speeches_date_df['date'])
  speeches_date_df['year'] = speeches_date_df['date'].dt.year
  speeches_date_df.drop('date', axis=1, inplace=True)

  speeches_year_count_df = speeches_date_df.groupby('year').count().reset_index().rename(columns={"i": "count"})

  #    year | count
  #    ------------
  #0   1995 | 2182
  return speeches_year_count_df

def build_all_speeches_df(docs_topics: list, all_speeches: list) -> pd.DataFrame:
  indexed_doc_topics = []

  for i, doc_topics in enumerate(docs_topics):
    for topic, weight in doc_topics:
      indexed_doc_topics.append(
        (i, all_speeches[i]['id'], all_speeches[i]['date'], topic, weight)
      )

  all_speeches_df = pd.DataFrame(indexed_doc_topics, columns=["index", "id", "date", "topic", "weight"])
  all_speeches_df['date'] = pd.to_datetime(all_speeches_df['date'])
  all_speeches_df['year'] = all_speeches_df['date'].dt.year
  all_speeches_df.drop('date', axis=1, inplace=True)

  return all_speeches_df


def build_top_speeches_for_topic_df(all_speeches: list, docs_topics: list, speeches_year_count_df: pd.DataFrame, num_top_topics: int, selected_topic: int):
  # FORMAT:
  # [(0, '1980-12-05', [21, 25, 88]),
  # (1, '1988-03-15', [78, 8, 87]),
  # (2, '1994-01-03', [60, 52, 7]),
  # (3, '1994-01-03', [27, 70, 81]),
  speeches_top_topics = [
    (
        i,
        s["date"],
        list(
          map(
            lambda x: x[0],
            sorted(docs_topics[i], key=lambda x: x[1], reverse=True)[0:num_top_topics] # top  topics
          )
        )
    )
    for i, s in enumerate(all_speeches)
  ]

  filtered_speeches = [
    (
      i,
      date,
      topics
    )
    for (i, date, topics) in speeches_top_topics
    if selected_topic in topics
  ]

  top_speeches_for_topic_df = pd.DataFrame(filtered_speeches, columns=["i", "date", "topics"])
  top_speeches_for_topic_df['date'] = pd.to_datetime(top_speeches_for_topic_df['date'])
  top_speeches_for_topic_df['year'] = top_speeches_for_topic_df['date'].dt.year

  df_grouped = top_speeches_for_topic_df[['year','i']].groupby('year').count().reset_index()

  df_grouped['top_speech_percentage'] = df_grouped['i'] * 100 / speeches_year_count_df.copy().reset_index()['count']

  return df_grouped


def run(model_name: str, speeches_all_preproc: str, outdir: str, num_top_topics: int) -> None:
  model = "data/models/{}/model".format(model_name)
  lda = LdaMallet.load(model)

  docs_topics = pickle.load(open("data/docs_topics_good_{}.pickle".format(model_name), "rb"))
  all_speeches = pickle.load(open(speeches_all_preproc, "rb"))

  bad_topics = get_bad_topics(model_name)
  speeches_year_count_df = build_speeches_year_count_df(all_speeches)
  all_speeches_df = build_all_speeches_df(docs_topics, all_speeches)

  save_frequency_all_plot(
    df=speeches_year_count_df,
    title="Contagem absoluta de discursos por ano",
    filename="{}/frequency_all.png".format(outdir)
  )
  save_topics_with_samples(lda, all_speeches, outdir)

  for topic in range(0, lda.num_topics):
    if topic not in bad_topics:
      topic_speeches_df = all_speeches_df[
        all_speeches_df['topic'] == topic
      ]

      top_speeches_for_topic_df = build_top_speeches_for_topic_df(all_speeches, docs_topics, speeches_year_count_df, num_top_topics, topic)

      generate_topic_plot(
        speeches_all_preproc=all_speeches,
        topic_speeches_df=topic_speeches_df,
        top_speeches_for_topic_df=top_speeches_for_topic_df,
        speeches_year_count_df=speeches_year_count_df,
        topic=topic,
        outdir=outdir,
        lda=lda
      )


if __name__ == '__main__':
  model_name               = "65_it_10000"
  speeches_all             = "data/speeches_all_preproc_filtered.pickle"
  outdir                   = "results/time_topics_average_{}".format(model_name)
  num_top_topics           = 1

  if os.path.exists(outdir):
    shutil.rmtree(outdir)
  os.makedirs(outdir)

  run(model_name, speeches_all, outdir, num_top_topics)
