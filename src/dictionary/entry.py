import json
from typing import NamedTuple, List, Dict


class EnglishDictEntry(NamedTuple):
    word: str
    paraphrases: List[str]
    pattern: str
    pronunciation: Dict[str, str]
    rank: str
    sentences: List[List]

    @classmethod
    def from_json(cls, json: dict) -> 'EnglishDictEntry':
        return cls(
            json['word'],
            json['paraphrases'],
            json['pattern'],
            json['pronunciation'],
            json['rank'],
            json['sentences']
        )

    def to_json(self) -> str:
        return json.dumps({
            'word': self.word,
            'paraphrases': self.paraphrases,
            'pattern': self.pattern,
            'pronunciation': self.pronunciation,
            'rank': self.rank,
            'sentences': self.sentences
        })


class ChineseDictEntry(NamedTuple):
    word: str
    desc: List
    paraphrases: List[str]
    pronunciation: str
    sentences: List[List[str]]

    @classmethod
    def from_json(cls, json: dict) -> 'EnglishDictEntry':
        return cls(
            json['word'],
            json['desc'],
            json['paraphrases'],
            json['pronunciation'],
            json['sentences']
        )

    def to_json(self) -> str:
        return json.dumps({
            'word': self.word,
            'desc': self.desc,
            'paraphrases': self.paraphrases,
            'pronunciation': self.pronunciation,
            'sentences': self.sentences
        })
