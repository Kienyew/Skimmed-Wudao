#!/usr/bin/env python3

import argparse
import itertools
from concurrent import futures
from pathlib import Path

from dictionary import Dictionary

dictionary = Dictionary()


def worker(word: str):
    try:
        dictionary.query_word(word)
        return word
    except Exception as e:
        return (word, e)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        'generate.py', description='fetch definition of words in the given file, each word seperate by a new line.')
    argparser.add_argument('files', nargs='+')
    args = argparser.parse_args()
    words = [*itertools.chain(*(Path(file).read_text().splitlines() for file in args.files))]

    # sqlite3 cannot manage connection from multiple thread
    with futures.ProcessPoolExecutor(max_workers=16) as executor:
        for result in executor.map(worker, words):
            if isinstance(result, str):
                word = result
                print(f"Inserted '{word}' into database.")
            else:
                word, error = result
                print(f"Error on '{word}': {error}")
