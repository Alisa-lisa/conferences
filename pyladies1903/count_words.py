from pyladies_wordcount import *
import re


def simple_count(file):
    res = 0
    with open(file) as f:
        for line in f:
            if re.findall(r"\bAlice|ALICE\b", line):
                res += 1
    return res


def fast_count(file):
    return sum(1 for match in re.finditer(r"\bAlice|ALICE\b", open(file).read()))


def magic_count(file, simple=True):
    if simple:
        return WordCounter(file).search_sequential("Alice")
    else:
        return WordCounter(file).search("Alice")

