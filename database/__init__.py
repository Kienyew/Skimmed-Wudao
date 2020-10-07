import gzip
import sqlite3
from pathlib import Path
from typing import Optional

from xdg import BaseDirectory
from dictionary.entry import EnglishDictEntry, ChineseDictEntry


class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        Path(self.db_path).touch(0o644, exist_ok=True)
        self.database = sqlite3.connect(self.db_path)
        self.cursor = self.database.cursor()
        self.init_database()

    def init_database(self):
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS english(word TEXT PRIMARY KEY, gzipped_json BLOB)')
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS chinese(word TEXT PRIMARY KEY, gzipped_json BLOB)')
        self.database.commit()

    def query_english_word_json(self, word: str) -> Optional[str]:
        self.cursor.execute(
            'SELECT gzipped_json FROM english WHERE word=?', [word])
        fetched = self.cursor.fetchone()
        if fetched is None:
            return None

        json_text = gzip.decompress(fetched[0])
        return json_text

    def query_chinese_word_json(self, word: str) -> Optional[str]:
        self.cursor.execute(
            'SELECT gzipped_json FROM chinese WHERE word=?', [word])
        fetched = self.cursor.fetchone()
        if fetched is None:
            return None

        json_text = gzip.decompress(fetched[0])
        return json_text

    def insert_english_entry(self, entry: EnglishDictEntry):
        gzipped_json = gzip.compress(entry.to_json().encode())
        self.cursor.execute(
            'INSERT INTO english (word, gzipped_json) VALUES (?, ?)', (entry.word, gzipped_json))
        self.database.commit()

    def insert_chinese_entry(self, entry: ChineseDictEntry):
        gzipped_json = gzip.compress(entry.to_json().encode())
        self.cursor.execute(
            'INSERT INTO chinese (word, gzipped_json) VALUES (?, ?)', (entry.word, gzipped_json))
        self.database.commit()


__running_database: DatabaseManager = None


def get_default_database() -> DatabaseManager:
    global __running_database

    if __running_database is None:
        db_path = Path(BaseDirectory.save_cache_path(
            'skimmed-wudao')) / 'wudao-database.sqlite3'
        __running_database = DatabaseManager(db_path)

    return __running_database
