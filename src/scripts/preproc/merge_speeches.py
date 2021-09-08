import pickle

def merge_dicts_overwrite_empty(d1: dict, d2: dict):
  result = d2.copy()
  result.update({k:v for k,v in d1.items() if v is not None})
  return result

def merge(outdir: str) -> None:
  speeches_leg  = pickle.load(open('data/speeches_all_legislature.pickle', 'rb'))
  speeches_date = pickle.load(open('data/speeches_all_date.pickle', 'rb'))

  print("Speeches by leg size: {}".format(len(speeches_leg)))
  print("Speeches by date size: {}".format(len(speeches_date)))

  # transform each speech into correct dict format
  speeches_leg_processed = []
  speeches_date_processed = []

  match_count = 0

  for speech in speeches_leg:
    id           = speech.get("CodigoPronunciamento")
    text         = speech.get("Conteudo")
    date         = speech.get("DataPronunciamento")
    keywords     = speech.get("Indexacao")
    party        = speech.get("SiglaPartidoParlamentarNaData")
    state        = speech.get("UfParlamentarNaData")
    senator      = speech.get("IdentificacaoParlamentar", {}).get("NomeCompletoParlamentar")
    senator_id   = speech.get("IdentificacaoParlamentar", {}).get("CodigoParlamentar")
    speech_type  = speech.get("TipoUsoPalavra", {}).get("Sigla")
    session_type = speech.get("SessaoPlenaria", {}).get("SiglaTipoSessao")

    new_speech = {
      "id":           id,
      "text":         text,
      "date":         date,
      "keywords":     keywords,
      "party":        party,
      "senator":      senator,
      "senator_id":   senator_id,
      "state":        state,
      "speech_type":  speech_type,
      "session_type": session_type,
    }

    speeches_leg_processed.append(new_speech)

  for speech in speeches_date:
    id           = speech.get("CodigoPronunciamento")
    text         = speech.get("Conteudo")
    date         = speech.get("Data")
    keywords     = speech.get("Indexacao")
    party        = speech.get("Partido")
    senator      = speech.get("NomeAutor")
    senator_id   = speech.get("CodigoParlamentar")
    state        = speech.get("UF")
    speech_type  = speech.get("TipoUsoPalavra", {}).get("Sigla")
    session_type = speech.get("Sessao", {}).get("TipoSessao")

    new_speech = {
      "id":           id,
      "text":         text,
      "date":         date,
      "keywords":     keywords,
      "party":        party,
      "senator":      senator,
      "senator_id":   senator_id,
      "state":        state,
      "speech_type":  speech_type,
      "session_type": session_type,
    }

    speeches_date_processed.append(new_speech)


  speeches_merged = speeches_leg_processed.copy()
  speeches_merged_ids = [s["id"] for s in speeches_merged]

  for speech in speeches_date_processed:
    if speech["id"] not in speeches_merged_ids:
      speeches_merged.append(speech)

  # for speech_date in speeches_date_processed:
    # for speech_leg in speeches_leg_processed:


  for speech in speeches_date_processed:
    match = [(i, s) for i, s in enumerate(speeches_leg_processed) if s["id"] == speech["id"]]

    if len(match) == 1:
      [(matched_index, matched_speech)] = match
      merged_speech = merge_dicts_overwrite_empty(matched_speech, speech)

      speeches_merged[matched_index] = merged_speech
      match_count = match_count + 1

    else:
      speeches_merged.append(speech)

  print("Merged speeches size: {}".format(len(speeches_merged)))
  print("Matches: {}".format(match_count))

  with open('{}/speeches_all_merged.pickle'.format(outdir), 'wb') as handle:
    pickle.dump(speeches_merged, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
  outdir = "data"
  merge(outdir)