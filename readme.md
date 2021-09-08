# Brazilian Senator Speeches

## Speech data

- Preprocessed senator speeches from 1995 to 2019 with metadata are contained in [senator_speeches.pickle](senator_speeches.pickle) in the root directory.

## Steps to execute

0. Install deps
   `pip install -r requirements.txt`

1. Crawl

   - 1.1 `src/scripts/crawler/crawl_by_date.py`

   - 1.2 `src/scripts/crawler/crawl_by_legislature.py`

     - Populates data/speeches_raw_date/\*.json and data/speeches_raw_legislature/\*.json with speeches.

   - 1.3 `src/scripts/crawler/speech_bundler.py`

     - Combines all json speeches into one file (~ 500mb) for date, legislature;
     - Applies some filters (e.g.: speech_type);
     - Creates `speeches_all_legislature.pickle`, `speeches_all_date.pickle` file.

2. Preproc

   - 2.0 `src/scripts/preproc/merge_scripts.py`

     - Combines `speeches_all_legislature.pickle` and `speeches_all_date.pickle` into one 1gb file: `speeches_all_merged.pickle`.
     - Applies field standards.

   - 2.1 `src/scripts/preproc/generate_stopwords.py`

     - Generates `stopword.txt` from various sources;

   - 2.2 `src/scripts/preproc/preproc.py`

     - Takes ~ 5h;
     - Runs preproc on `speeches_all_merged.pickle`;
     - Creates `speeches_preproc.pickle`;

   - 2.3 `src/scripts/preproc/save_all_preproc_filtered.py`

     - Applies some filters on preprocessed data;
     - Creates `speeches_all_preproc_filtered.pickle`: this is the same as `senator_speeches.pickle` found in the root directory.

3. LDA

   - 3.1 `src/scripts/lda/save_corpus_dict.py`

     - Uses `speeches_all_preproc_filtered.pickle` to create a corpus and a dictionary, to be used by LDA;
     - Will remove frequent and infrequent words.

   - 3.2 `src/scripts/lda/lda.py`

     - Uses `speeches_all_preproc_filtered.pickle`, `corpus.pickle` and `dictionary.pickle`.
     - Creates MALLET LDA model.

4. Analysis

   - 4.1 `src/scripts/analysis`
     - Contains multiple data analysis scripts.
