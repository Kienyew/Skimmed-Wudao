from typing import Optional

from utils import online_query
from dictionary.entry import EnglishDictEntry, ChineseDictEntry


def query_english_word(word: str) -> Optional[EnglishDictEntry]:
    return online_query.get_en_text(word)


def query_chinese_word(word: str) -> Optional[ChineseDictEntry]:
    return online_query.get_zh_text(word)
