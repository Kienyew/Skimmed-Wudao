#!/usr/bin/env python3

import sys
import itertools
import argparse
from typing import List, Iterator

import database
from utils import language
from dictionary import Dictionary
from painter import Painter


def get_completion_words(sql_like_statement: str) -> Iterator[str]:
    escaped_word = ''.join(
        c for c in sql_like_statement if c not in ['%', '_'])
    db_manager = database.get_default_database()
    if language.get_language(escaped_word) == language.Lang.ENGLISH:
        db_manager.cursor.execute(
            'SELECT word FROM english WHERE word LIKE ?', sql_like_statement)
    else:
        db_manager.cursor.execute(
            'SELECT word FROM chinese WHERE word LIKE ?', sql_like_statement)

    return itertools.chain(*db_manager.cursor.fetchall())


def parse_args(argv: List[str]) -> argparse.ArgumentParser:
    argparser = argparse.ArgumentParser('wd')
    argparser.add_argument('words', action='store',
                           nargs='*', help='word[s] to search')

    argparser.add_argument('--color', '-c', choices=[
                           'always', 'never'], default='always', help='whether to paint color on output')

    argparser.add_argument('--local', '-l', action='store_true',
                           default=False, help='only search in local database')

    argparser.add_argument('--completion', nargs=1,
                           help='print the words for shell completion script, feed to the SQL LIKE statement')

    args = argparser.parse_args(argv[1:])

    if len(args.words) == 0 and args.completion is None:
        argparser.print_help()
        sys.exit(1)

    return args


def main():
    args = parse_args(sys.argv)
    if args.words:
        word = ' '.join(args.words)
        entry = Dictionary(args.local).query_word(word)
        output = Painter(color=args.color == 'always').paint_entry(entry)
        print(output)
    elif args.completion:
        for word in get_completion_words(args.completion):
            print(word)
    else:
        raise NotImplementedError('code should not reach here')


if __name__ == '__main__':
    main()
