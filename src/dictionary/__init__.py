from typing import Optional, Union

import database
from utils import language
from . import local, online
from .entry import ChineseDictEntry, EnglishDictEntry


class Dictionary:
    def __init__(self, local_only=False, db_feedback=True):
        self.local_only = local_only
        self.db_feedback = db_feedback
        self.database = database.get_default_database()

    def query_english_word(self, word: str) -> Optional[EnglishDictEntry]:
        entry = local.query_english_word(word)
        if entry is not None or self.local_only:
            return entry

        entry = online.query_english_word(word)
        if entry is None:
            return None

        return entry

    def query_chinese_word(self, word: str) -> Optional[ChineseDictEntry]:
        entry = local.query_chinese_word(word)
        if entry is not None or self.local_only:
            return entry

        entry = online.query_chinese_word(word)
        if entry is None:
            return None

        return entry

    def query_word(self, word: str) -> Optional[Union[ChineseDictEntry, EnglishDictEntry]]:
        if language.get_language(word) == language.Lang.CHINESE:
            entry = self.query_chinese_word(word)
            if self.db_feedback:
                self.database.insert_chinese_entry(entry)
        elif language.get_language(word) == language.Lang.ENGLISH:
            entry = self.query_english_word(word)
            if self.db_feedback:
                self.database.insert_english_entry(entry)

        return entry
