import re
import enum


class Lang(enum.Enum):
    CHINESE = 'chinese'
    ENGLISH = 'english'


def get_language(word: str) -> Lang:
    if re.match(r'[\u4e00-\u9fff]+', word):
        return Lang.CHINESE
    else:
        return Lang.ENGLISH
