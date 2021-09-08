# pip install gensim==3.8.1 --user

import pickle
from gensim.models.wrappers import LdaMallet
import numpy as np
import pandas as pd
import os
import shutil
import datetime
from topics import run as save_topic_list, save_topics_with_samples
from lda_utils import get_docs_topics

def display_single_lda_topic(lda: LdaMallet, topic: int):
  topic = ", ".join([x[0] for x in lda.show_topic(topic)])

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


def save_frequency_plot(df: pd.DataFrame, title: str, filename: str) -> None:
  plot = df.plot(marker='o', linestyle='-', grid=True, figsize=(17,7))

  plot.set_title(title)

  xticks = df.index.to_list()
  plot.set_xticks(xticks)
  # yticks = df_grouped.values.tolist()
  # plot.set_yticks(yticks)

  plot.xaxis.set_tick_params(rotation=45)
  plot.patch.set_facecolor('white')

  fig = plot.get_figure()
  # fig.autofmt_xdate(bottom=0.2, rotation=90, ha='right')

  fig.savefig(filename)
  fig.clf()


def generate_topic_plot(
  speeches_all_preproc,
  speeches_topics,
  topic,
  outdir: str,
  lda: LdaMallet,
):

  filtered_speeches = [
      (
          id,
          date,
          topics
      )
      for (id, date, topics) in speeches_topics
      if topic in topics
  ]

  # all speeches
  df_year_all = pd.DataFrame([
      (i, d,  None)
      for (i, d, t) in speeches_topics
  ], columns=["id", "date", "topics"])
  df_year_all['date'] = pd.to_datetime(df_year_all['date'])
  df_year_all['year'] = df_year_all['date'].dt.year
  df_year_all_grouped = df_year_all[['year','id']].groupby('year').count()


  # generate frequency per year for all topics
  if topic == 0:
    save_frequency_plot(
      df=df_year_all_grouped,
      title="Absolute speech frequency",
      filename="{}/frequency_all.png".format(outdir)
    )
    # save_topic_list(lda, outdir, "")
    save_topics_with_samples(lda, speeches_all_preproc, outdir)

  # filtered
  df = pd.DataFrame(filtered_speeches, columns=["id", "date", "topics"])
  df['date'] = pd.to_datetime(df['date'])
  df['year'] = df['date'].dt.year

  df_grouped = df[['year','id']].groupby('year').count()
  df_grouped["Total"] = df_year_all[['year','id']].groupby('year').count()
  df_grouped['Percentage'] = df_grouped['id'] * 100 /df_grouped['Total']

  df_grouped = df_grouped['Percentage']

  # df.info()

  save_frequency_plot(
    df=df_grouped,
    title="Relative speech frequency - topic {}\n{}".format(topic, display_single_lda_topic(lda, topic)),
    filename="{}/topic_{}.png".format(outdir, topic)
  )

def run(model: str, speeches_all_preproc: str, outdir: str, topic_threshold: int) -> None:

  os.chdir("X:/Victor/Documents/TCC/new_discursos/src")

  lda = LdaMallet.load(model)
  lda.mallet_path = "lib\\mallet-2.0.8\\bin\\mallet"

  os.environ['MALLET_HOME'] = 'X:\\Programs\\Java\\mallet\\mallet-2.0.8'

  docs_topics = get_docs_topics(lda)

  all_speeches = pickle.load(open(speeches_all_preproc, "rb"))

  dates = [
    (i, s["date"])
    for i, s in enumerate(all_speeches)
  ]

  sorted_dates = sorted(
    dates,
    key=lambda x: x[1]
  )

  speeches_topics = [
    (id, date, docs_topics[id])
    for (id, date) in sorted_dates
  ]

  speeches_top_topics = [
    (
        id,
        date,
        sorted(topics, key=lambda x: x[1], reverse=True)[0:topic_threshold] # top  topics
    )
    for (id, date, topics) in speeches_topics
  ]

  # [(32151, '1980-12-05', [21, 25, 88]),
  # (39526, '1988-03-15', [78, 8, 87]),
  # (13169, '1994-01-03', [60, 52, 7]),
  # (51924, '1994-01-03', [27, 70, 81]),
  speeches_topic_list = [
    (
        id,
        date,
        [topic[0] for topic in topics]
    )
    for (id, date, topics) in speeches_top_topics
]

  for topic in range(0, lda.num_topics):
    generate_topic_plot(
      speeches_all_preproc=all_speeches,
      speeches_topics=speeches_topic_list,
      topic=topic,
      outdir=outdir,
      lda=lda
    )


if __name__ == '__main__':
  model_name               = "20_it_10000_NDL"
  model                    = "data/models/{}/model".format(model_name)
  speeches_all_preproc     = "data/speeches_all_preproc_filtered_NDL.pickle"
  outdir                   = "results/time_topics_{}".format(model_name)
  topic_threshold          = 3 # top 1 topics

  if os.path.exists(outdir):
    shutil.rmtree(outdir)
  os.makedirs(outdir)

  run(model, speeches_all_preproc, outdir, topic_threshold)