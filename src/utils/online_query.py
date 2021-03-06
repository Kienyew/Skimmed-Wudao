from typing import Optional

from dictionary.entry import EnglishDictEntry, ChineseDictEntry


def get_word_html(x):
    import requests
    return requests.get(f'http://dict.youdao.com/search?q={x}').text


def multi_space_to_single(text):
    cursor = 0
    result = ""
    while cursor < len(text):
        if text[cursor] in ["\t", " ", "\n", "\r"]:
            while text[cursor] in ["\t", " ", "\n", "\r"]:
                cursor += 1
            result += " "
        else:
            result += text[cursor]
            cursor += 1
    return result


# get word info online
def get_en_text(word) -> Optional[EnglishDictEntry]:
    import bs4
    content = get_word_html(word)
    word_struct = {"word": word}
    root = bs4.BeautifulSoup(content, 'lxml')

    if root.select_one('.keyword') is None:
        return None

    pron = {}

    pron_fallback = False

    for pron_item in root.select(".pronounce"):
        pron_lang = None
        pron_phonetic = None

        for sub_item in pron_item.children:
            if isinstance(sub_item, str) and pron_lang is None:
                pron_lang = sub_item
                continue
            if isinstance(sub_item, bs4.Tag) and sub_item.name.lower() == "span" and sub_item.has_attr(
                    "class") and "phonetic" in sub_item.get("class"):
                pron_phonetic = sub_item
                continue
        if pron_phonetic is None:
            # raise SyntaxError("WHAT THE FUCK?")
            pron_fallback = True
            break
        if pron_lang is None:
            pron_lang = ""
        pron_lang = pron_lang.strip()
        pron_phonetic = pron_phonetic.text

        pron[pron_lang] = pron_phonetic

    if pron_fallback:
        for item in root.select(".phonetic"):
            if item.name.lower() == "span":
                pron[""] = item.text
                break

    word_struct["pronunciation"] = pron
    #
    #  <--  BASIC DESCRIPTION
    #
    nodes = root.select( "#phrsListTab .trans-container ul")
    basic_desc = []

    if len(nodes) != 0:
        ul = nodes[0]
        for li in ul.children:
            if not (isinstance(li, bs4.Tag) and li.name.lower() == "li"):
                continue
            basic_desc.append(li.text.strip())
    word_struct["paraphrase"] = basic_desc

    if not word_struct["paraphrase"]:
        d = root.select(".wordGroup.def")
        p = root.select(".wordGroup.pos")
        ds = ""
        dp = ""
        if len(d) > 0:
            ds = d[0].text.strip()
        if len(p) > 0:
            dp = p[0].text.strip()
        word_struct["paraphrase"] = (dp + " " + ds).strip()
    #
    #  -->
    #  <--  RANK
    #
    rank = ""
    nodes = root.select(".rank")
    if len(nodes) != 0:
        rank = nodes[0].text.strip()
    word_struct["rank"] = rank
    #
    #  -->
    #  <-- PATTERN
    #
    # .collinsToggle .pattern
    pattern = ""

    nodes = root.select(".collinsToggle .pattern")
    if len(nodes) != 0:
        #    pattern = nodes[0].text.strip().replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
        pattern = multi_space_to_single(nodes[0].text.strip())
    word_struct["pattern"] = pattern
    #
    #  -->
    #  <-- VERY COMPLEX
    #
    word_struct["sentence"] = []
    for child in root.select(".collinsToggle .ol li"):
        p = child.select("p")
        if len(p) == 0:
            continue
        p = p[0]
        desc = ""
        cx = ""
        for node in p.children:
            if isinstance(node, str):
                desc += node
            elif isinstance(node, bs4.Tag) and node.name.lower() == "b" and node.children:
                for x in node.children:
                    if isinstance(x, str):
                        desc += x
            elif isinstance(node, bs4.Tag) and node.name.lower() == "span":
                cx = node.text
        desc = multi_space_to_single(desc.strip())

        examples = []

        for el in child.select(".exampleLists"):
            examp = []
            for p in el.select(".examples p"):
                examp.append(p.text.strip())
            examples.append(examp)
        word_struct["sentence"].append([desc, cx, examples])
    # 21 new year
    if not word_struct["sentence"]:
        for v in root.select("#bilingual ul li"):
            p = v.select("p")
            ll = []
            for p in v.select("p"):
                if len(p) == 0:
                    continue
                if 'class' not in p.attrs:
                    ll.append(p.text.strip())
            if len(ll) != 0:
                word_struct["sentence"].append(ll)
    #  -->

    return EnglishDictEntry(word_struct['word'],
                            word_struct['paraphrase'],
                            word_struct['pattern'],
                            word_struct['pronunciation'],
                            word_struct['rank'],
                            word_struct['sentence'])


def get_zh_text(word) -> Optional[ChineseDictEntry]:
    import bs4
    content = get_word_html(word)
    word_struct = {"word": word}
    root = bs4.BeautifulSoup(content, 'lxml')
    if root.select_one('.keyword') is None:
        return None

    # pronunciation
    pron = ''
    for item in root.select(".phonetic"):
        if item.name.lower() == "span":
            pron = item.text
            break

    word_struct["pronunciation"] = pron

    #  <--  BASIC DESCRIPTION
    nodes = root.select("#phrsListTab .trans-container ul p")
    basic_desc = []

    if len(nodes) != 0:
        for li in nodes:
            basic_desc.append(li.text.strip().replace('\n', ' '))
    word_struct["paraphrase"] = basic_desc

    # DESC
    desc = []
    for child in root.select('#authDictTrans ul li ul li'):
        single = []
        sp = child.select('span')
        if sp:
            span = sp[0].text.strip().replace(':', '')
            if span:
                single.append(span)
        ps = []
        for p in child.select('p'):
            ps.append(p.text.strip())
        if ps:
            single.append(ps)
        desc.append(single)

    word_struct["desc"] = desc

    #  <-- VERY COMPLEX
    word_struct["sentence"] = []
    # 21 new year
    for v in root.select("#bilingual ul li"):
        p = v.select("p")
        ll = []
        for p in v.select("p"):
            if len(p) == 0:
                continue
            if 'class' not in p.attrs:
                ll.append(p.text.strip())
        if len(ll) != 0:
            word_struct["sentence"].append(ll)

    return ChineseDictEntry(word_struct['word'],
                            word_struct['desc'],
                            word_struct['paraphrase'],
                            word_struct['pronunciation'],
                            word_struct['sentence'])
