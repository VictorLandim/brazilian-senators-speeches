import os
import shutil
import pickle
from gensim.models.wrappers import LdaMallet
from timeit import default_timer as timer
from datetime import timedelta
import time
import lda_utils
import file_utils
import sample
import topics
import party


def get_out_folder(model_name: str) -> str:
    out_folder = "results/topics/{}".format(
        model_name
    )

    file_utils.recreate_folder(out_folder)

    return out_folder


def main(model_names: [], corpus: [], texts_raw: [], texts_preproc: []) -> None:
    """
    Main result pipeline.
    Generate results for every model specified.
    """

    for (model_name) in model_names:
        print("[main] generating results for: {}".format(
            model_name
        ))

        out_folder = get_out_folder(model_name)
        model_path = "data/models/{}/model".format(model_name)
        lda = LdaMallet.load(model_path)

        topics.run(lda, out_folder, model_name)

        sample_ids = [32279, 14557, 26335, 52979, 51620]
        sample.run(lda, model_name, texts_raw,
                   texts_preproc, out_folder, sample_ids=sample_ids)

        party.run(lda, out_folder, model_name, texts_raw)

        shutil.make_archive(model_name, 'zip', out_folder)


if __name__ == "__main__":
    model_names = [
        "lda_model_50_stem_it_10000",
    ]

    start_time = timer()

    texts_raw = lda_utils.get_texts_raw()
    print("[main] fetch texts raw")

    texts_preproc = lda_utils.get_texts_preproc()
    print("[main] fetch texts preproc")

    main(model_names, [], texts_raw, texts_preproc)

    end_time = timer()

    print("Model results created, took {}".format(
        timedelta(seconds=end_time-start_time)
    ))
