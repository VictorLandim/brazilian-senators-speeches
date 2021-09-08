import os
import shutil
from datetime import date
from typing import TextIO


def recreate_folder(folder):
    """
    Creates `folder` if doesn't exist, deletes
    and creates again otherwise.
    """

    if not os.path.exists(folder):
        os.makedirs(folder)

    else:
        shutil.rmtree(folder, ignore_errors=True)
        os.makedirs(folder)


def write_separator(f: TextIO) -> None:
    """
    Print separator string used in files.
    """

    f.write("===============================================\n")


def write_header(file: TextIO, model_name: str, close=True) -> None:
    """
    Writes default header to result files.
    If `close=True`, writes a final separator.
    """
    write_separator(file)

    file.write("Date: {}.\n".format(
        date.today().strftime("%B %d, %Y")
    ))

    file.write("Model used: {}.\n".format(
        model_name
    ))

    if close:
        write_separator(file)
        file.write("\n")
