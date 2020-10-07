#!/usr/bin/env python3

import sys
import argparse

from dictionary import Dictionary
from painter import Painter


def main():
    argparser = argparse.ArgumentParser('wd')
    argparser.add_argument('words', action='store',
                           nargs='+', help='word[s] to search')
    argparser.add_argument(
        '--color', '-c', choices=['always', 'never'], default='always', help='whether to paint color on output')
    argparser.add_argument('--local', '-l', action='store_true',
                           default=False, help='only search in local database')
    args = argparser.parse_args(sys.argv[1:])

    word = ' '.join(args.words)
    entry = Dictionary(args.local).query_word(word)
    output = Painter(color=args.color == 'always').paint_entry(entry)
    print(output)


if __name__ == '__main__':
    main()
