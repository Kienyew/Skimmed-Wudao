import json
from typing import Optional

import database
from dictionary.entry import EnglishDictEntry, ChineseDictEntry


def query_english_word(word: str) -> Optional[EnglishDictEntry]:
    _database = database.get_default_database()
    entry_json = _database.query_english_word_json(word)
    if entry_json is None:
        return None

    return EnglishDictEntry.from_json(json.loads(entry_json))


def query_chinese_word(word: str) -> Optional[ChineseDictEntry]:
    _database = database.get_default_database()
    entry_json = _database.query_chinese_word_json(word)
    if entry_json is None:
        return None

    return ChineseDictEntry.from_json(json.loads(entry_json))
