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

def crawl_senator_speeches(leg: int, folder: str, processed_senators: list):
    """
    First crawls all senators, then crawls each one's speeches.
    """

    # senators processed in this iteration
    new_senators = []

    senator_url = "https://legis.senado.leg.br/dadosabertos/senador/lista/legislatura/{}".format(
      leg
    )
    speech_url = "https://legis.senado.leg.br/dadosabertos/senador/{}/discursos?casa=SF"
    # speech_url = "https://legis.senado.leg.br/dadosabertos/senador/{}/discursos?casa=SF&tipoSessao=DOR"
    # speech_url = "https://legis.senado.leg.br/dadosabertos/senador/{}/discursos?casa=SF&tipoSessao=NDL"


    headers = {"Accept": "application/json"}
    timeout=50

    speech_count = 0
    speeches_fail = []

    senator_response = requests_retry_session().get(senator_url, headers=headers, timeout=timeout)
    senator_json = json.loads(senator_response.content)
    senator_info = senator_json["ListaParlamentarLegislatura"]

    senator_list = senator_info["Parlamentares"]["Parlamentar"] if "Parlamentares" in senator_info else []

    for i, senator in enumerate(senator_list):
      print("- Senator {}/{} | leg {}".format(
        i,
        len(senator_list),
        leg
      ))
      senator_id = senator["IdentificacaoParlamentar"]["CodigoParlamentar"]

      if senator_id in processed_senators:
        continue

      speech_response = requests_retry_session().get(
        speech_url.format(senator_id),
        headers=headers, timeout=timeout
      )
      speech_json = json.loads(speech_response.content)
      speech_list = speech_json["DiscursosParlamentar"]

      if not "Parlamentar" in speech_list:
        continue

      senator_data = speech_list["Parlamentar"]["IdentificacaoParlamentar"]
      speech_list = ensure_is_array(speech_list["Parlamentar"]["Pronunciamentos"]["Pronunciamento"])

      for speech in speech_list:

        content_url = speech["UrlTexto"]
        speech_id = speech["CodigoPronunciamento"]

        speech_filename = "./{}/{}.json".format(folder, speech_id)

        content_response = requests_retry_session().get(content_url, headers=headers, timeout=50)

        soup = BeautifulSoup(content_response.content, "html.parser")
        selector = 'div.texto-integral'

        if not soup.select_one(selector):
          speeches_fail.append(speech_id)
          continue

        soup_result = soup.select_one(selector)
        speech_text = soup_result.get_text().strip()

        speech_json = speech
        speech_json["IdentificacaoParlamentar"] = senator_data
        speech_json["Conteudo"]  = speech_text

        with open(speech_filename, 'w+', encoding='utf8') as handle:
          json.dump(speech_json, handle, indent=4, sort_keys=True, ensure_ascii=False)
        speech_count += 1

      new_senators.append(senator_id)

    return speech_count, speeches_fail, new_senators


if __name__ == '__main__':

  leg_start = 1
  leg_end   = 57

  folder = "./data/speeches_raw_legislature"

  # shutil.rmtree(folder)
  # Path(folder).mkdir(parents=True, exist_ok=True)

  print("Crawling senator speeches from leg {} to leg {}.\n".format(
    leg_start, leg_end
  ))

  start_time = time.time()

  total_count = 0
  all_failed = []
  processed_senators = []

  for leg in range(leg_start, leg_end + 1):
    print("-- Crawling legislature {}, senators proc {}".format(leg, len(processed_senators)))
    speech_count, speeches_fail, new_senators = crawl_senator_speeches(leg, folder, processed_senators)

    total_count += speech_count
    all_failed += speeches_fail
    processed_senators += new_senators

  elapsed_time = int(time.time() - start_time)

  all_failed = set(all_failed)

  report_filename = './{}/crawler_report_legislature.txt'.format(folder)
  elapsed_msg = "Elapsed time: {:02d}h:{:02d}m:{:02d}s\n".format(
          elapsed_time // 3600, (elapsed_time % 3600 // 60), elapsed_time % 60)

  print("Crawler finished.\n{}".format(elapsed_msg))

  with open(report_filename, 'w+') as f:
      f.write("TEXT CRAWLER REPORT\n\n")
      f.write('Crawled at: {}\n'.format(date.today().strftime("%B %d, %Y")))

      f.write(elapsed_msg)

      f.write("\n\n== Speeches - total: {} ==\n".format(
          len(all_failed) + total_count))
      f.write("Failed: {}\n".format(len(all_failed)))
      f.write(str(all_failed))
