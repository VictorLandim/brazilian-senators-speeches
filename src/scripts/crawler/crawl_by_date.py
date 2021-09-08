import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
import time
from bs4 import BeautifulSoup
import pickle
import os.path
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from pathlib import Path
import shutil

def ensure_is_array(value):
    return [value] if not isinstance(value, list) else value

def requests_retry_session(
    retries=50,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def crawl_speeches(start_date, end_date, folder: str):
    """
    Crawl public speeches from Brazilian senators, from start date until end date.
    Will crawl only speeches with TipoUsoPalavra == "DIS" (Discurso)
    """

    start_time = time.time()

    # url = "https://legis.senado.leg.br/dadosabertos/plenario/lista/discursos/{}/{}?siglaCasa=SF&tipoSessao=DOR"
    url = "https://legis.senado.leg.br/dadosabertos/plenario/lista/discursos/{}/{}?siglaCasa=SF"

    headers = {"Accept": "application/json"}
    timeout=50

    speech_count = 0
    speeches_fail = []

    date_offset = relativedelta(months=+1)

    current_start_date = start_date
    current_end_date = start_date + date_offset

    # emulate do-while loop
    while True:

      start_str = current_start_date.strftime("%Y%m%d")
      end_str = current_end_date.strftime("%Y%m%d")

      current_url = url.format(
        start_str,
        end_str
      )

      print("[CRAWLING] {}".format(current_url))

      response = requests_retry_session().get(current_url, headers=headers, timeout=timeout)

      if "Sessoes" in json.loads(response.content)["DiscursosSessao"]:
        session_list = json.loads(response.content)["DiscursosSessao"]["Sessoes"]["Sessao"]
        session_list = ensure_is_array(session_list)

        for session in session_list:
          if not "Pronunciamento" in session["Pronunciamentos"]:
            continue

          pronunciamentos = ensure_is_array(session["Pronunciamentos"]["Pronunciamento"])
          session_data = session
          del session_data["Pronunciamentos"]

          for speech in pronunciamentos:

              speech_type = speech["TipoUsoPalavra"]["Sigla"]

              # https://legis.senado.leg.br/dadosabertos/senador/lista/tiposUsoPalavra
              # if not speech_type in ["DIS", "DISPUB", "DISPRES"]:
                  # continue

              content_url = speech["TextoIntegral"]
              speech_id = speech["CodigoPronunciamento"]

              speech_filename = "./{}/{}.json".format(folder, speech_id)

              content_response = requests_retry_session().get(content_url, headers=headers, timeout=50)

              soup = BeautifulSoup(content_response.content, "html.parser")
              selector = 'div.texto-integral'

              if not soup.select_one(selector):
                  speeches_fail.append(speech_id)
                  print("Failed: {}".format(content_url))
                  continue

              soup_result = soup.select_one(selector)
              speech_text = soup_result.get_text().strip()

              speech_json = speech
              speech_json["Conteudo"] = speech_text
              speech_json["Sessao"] = session_data

              with open(speech_filename, 'w+', encoding='utf8') as handle:
                json.dump(speech_json, handle, indent=4, sort_keys=True, ensure_ascii=False)
              speech_count += 1

      # exit condition
      # already crawled last end_date
      if current_end_date == end_date:
        break

      # update dates
      current_start_date += date_offset

      if current_end_date + date_offset >= end_date:
        current_end_date =  end_date
      else:
        current_end_date += date_offset


    elapsed_time = int(time.time() - start_time)

    report_filename = './{}/crawler_report_date.txt'.format(folder)
    elapsed_msg = "Elapsed time: {:02d}h:{:02d}m:{:02d}s\n".format(
            elapsed_time // 3600, (elapsed_time % 3600 // 60), elapsed_time % 60)

    print("Crawler finished.\n{}".format(elapsed_msg))

    with open(report_filename, 'w+') as f:
        f.write("TEXT CRAWLER REPORT\n\n")
        f.write('Crawled at: {}\n'.format(date.today().strftime("%B %d, %Y")))

        f.write(elapsed_msg)

        f.write("\n\n== Speeches - total: {} ==\n".format(
            len(speeches_fail) + speech_count))
        f.write("Failed: {}\n".format(len(speeches_fail)))
        f.write(str(speeches_fail))

if __name__ == '__main__':

  # democratic start
  start_date = datetime.strptime("1985/03/15", "%Y/%m/%d")
  # start_date = datetime.strptime("1995/07/15", "%Y/%m/%d")
  end_date = datetime.strptime("2020/12/31", "%Y/%m/%d")

  folder = "data/speeches_raw_date"

  shutil.rmtree(folder)
  Path(folder).mkdir(parents=True, exist_ok=True)

  print("Crawling senator speeches from {} to {}.".format(
    start_date.strftime("%Y/%m/%d"),
    end_date.strftime("%Y/%m/%d")
  ))

  crawl_speeches(start_date, end_date, folder)
