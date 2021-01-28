from typing import Union

from termcolor import colored as _colored
from dictionary.entry import ChineseDictEntry, EnglishDictEntry


def dummy_colored(text: str, *args, **kwargs):
    return text


class Painter:
    def __init__(self, color=True):
        self.color = color

    def paint_entry(self, entry: Union[ChineseDictEntry, EnglishDictEntry]) -> str:
        if isinstance(entry, EnglishDictEntry):
            return self.paint_english_entry(entry)
        elif isinstance(entry, ChineseDictEntry):
            return self.paint_chinese_entry(entry)
        else:
            raise TypeError('invalid type')

    def paint_english_entry(self, entry: EnglishDictEntry) -> str:
        colored = _colored if self.color else dummy_colored
        output_lines = []

        # word
        output_lines += [colored(entry.word, color='red')]

        # pronunciation
        if entry.pronunciation:
            pronunciation_output = ''
            if '' in entry.pronunciation:
                pronunciation_output = f"英/美 {colored(entry.pronunciation[''], color='cyan')}  "
            else:
                if '英' in entry.pronunciation:
                    pronunciation_output += f"英 {colored(entry.pronunciation['英'], color='cyan')}  "
                if '美' in entry.pronunciation:
                    pronunciation_output += f"美 {colored(entry.pronunciation['美'], color='cyan')}  "

            output_lines += [pronunciation_output]

        # paraphrases
        for paraphrase in entry.paraphrases:
            output_lines += [colored(paraphrase, color='blue')]

        # rank and pattern
        rank_and_pattern_output = ''
        if entry.rank:
            rank_and_pattern_output += colored(entry.rank, color='red') + '  '
        if entry.pattern:
            rank_and_pattern_output += colored(
                entry.pattern.strip(), color='red')

        output_lines += [rank_and_pattern_output]

        # sentences
        if entry.sentences:
            if len(entry.sentences[0]) == 2:
                collins_flag = False
            else:
                collins_flag = True

            if collins_flag:
                for i, v in enumerate(entry.sentences, 1):
                    if len(v) != 3:
                        continue

                    if v[1] == '' or len(v[2]) == 0:
                        continue

                    sentence = ''
                    if v[1].startswith('['):
                        sentence += f"{i}. {colored(v[1], color='green')}"
                    else:
                        sentence += f"{i}. {colored('[' + v[1] + ']', color='green')}"

                    sentence += v[0]
                    output_lines += [sentence]

                    for sv in v[2]:
                        output_lines += [
                            f"  {colored('例', color='green')}: {colored(sv[0] + ' ' + sv[1], color='yellow', attrs=['bold'])}"]

                    output_lines += ['']
            else:
                for i, v in enumerate(entry.sentences, 1):
                    if len(v) != 2:
                        continue

                    output_lines += [
                        f"{i}. {colored('[例]')} {v[0]}  {colored(v[1], color='yellow', attrs=['bold'])}"]

        return '\n'.join(output_lines)

    def paint_chinese_entry(self, entry: ChineseDictEntry) -> str:
        colored = _colored if self.color else dummy_colored

        output_lines = []
        # word
        output_lines += [colored(entry.word, color='red')]

        # pronunciation
        if entry.pronunciation:
            output_lines += [colored(entry.pronunciation, color='cyan')]

        if entry.paraphrases:
            for v in entry.paraphrases:
                v = v.replace('  ;  ', ', ')
                output_lines += [colored(v, color='blue')]

        # description
        if entry.desc:
            output_lines += ['']
            for i, v in enumerate(entry.desc, 1):
                if not v:
                    continue

                # sub title
                output_lines += [f"{i}. {colored(v[0], color='green')}"]

                # sub example
                if len(v) == 2:
                    for j in range(0, len(v[1]), 2):
                        line = f"    {colored(v[1][j].strip().replace(';', ''), color='yellow', attrs=['bold'])}    {v[1][j + 1]}"
                        output_lines += [line]

        # example
        if entry.sentences:
            output_lines += ['']
            output_lines += [colored('例句：', color='red')]
            for i, v in enumerate(entry.sentences, 1):
                if len(v) == 2:
                    output_lines += ['']
                    output_lines += [
                        f"{i}. {colored(v[0], color='yellow')}   {v[1]}"]

        return '\n'.join(output_lines)
