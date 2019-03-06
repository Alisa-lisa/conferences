from pyladies_wordcount import *
import re

def simple_count():
    res = 0
    with open('lol.txt') as f:
        for line in f:
            if re.findall(r"\bAlice|ALICE\b", line):
                res += 1
    return res

def fast_count():
    return sum(1 for match in re.finditer(r"\bAlice|ALICE\b", open("lol.txt").read()))

def magic_count(simple=True):
    if simple:
        return WordCounter("lol.txt").search_sequential("Alice")
    else:
        return WordCounter("lol.txt").search("Alice")

