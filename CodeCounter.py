import os
from pprint import pprint
from collections import defaultdict
from datetime import datetime
import time
import json

SCRIPT_DIR = os.path.dirname(__file__)
LANG_PYTHON = "Python"
LANG_C_CPP = "C/C++"
COUNT_INTERVAL = 60 #Seconds
KNOWN_EXT = {
    ".py" : LANG_PYTHON,
    ".pyw" : LANG_PYTHON,
    ".bat" : "Batch",
    ".cmd" : "Batch",
    ".c" : LANG_C_CPP,
    ".h" : LANG_C_CPP,
    ".hpp" : LANG_C_CPP,
    ".cpp" : LANG_C_CPP,
    ".cc" : LANG_C_CPP,
    ".php" : "PHP",
    ".php3" : "PHP",
    ".php4" : "PHP",
    ".pl" : "Pearl",
    ".js" : "JavaScript",
    ".ts" : "TypeScript",
    ".java" : "Java",
    ".cs" : "C#",
    ".sh" : "Bash",
}


def detect_lang(fpath):
    _, ext = os.path.splitext(fpath)
    ext = ext.lower()

    lang = KNOWN_EXT.get(ext)
    if lang is not None:
        return lang

    fname = os.path.basename(fpath).lower()
    if fname == "Makefile" or fname.startswith("makefile."):
        return "Makefile"
    
    return None


def count_loc(fpath, lang):
    with open(fpath, encoding="ibm437") as f:
        data = f.read()
    
    loc = 0
    for line in data.splitlines():
        line = line.strip()
        if line == "":
            continue

        if lang == LANG_PYTHON:
            if line.startswith("#"):
                continue
        elif lang == LANG_C_CPP:
            if line.startswith("//"):
                continue
    
        loc += 1

    return loc

def count_locs_in_path(code_path):
    now = datetime.now()
    stats = defaultdict(int)
    total_loc = 0

    for path, dirs, files in os.walk(f"{code_path}"):
        print(path)
        for fname in files:
            fpath = f"{path}/{fname}"
            lang = detect_lang(fpath)

            if lang is None:
                #print(fname)
                continue

            loc = count_loc(fpath, lang)

            stats[lang] += loc

            #print(" ", fname, "<--", lang, loc)
            total_loc += loc

    date = now.strftime("%Y-%m-%d %H:%M")
    #print("-" * 70, date)
    #pprint(dict(stats))
    #print(f"Total: {total_loc}")

    return {
        "date" : date,
        "total" : total_loc,
        "stats" : dict(stats)
    }

stats_fpath = f"{SCRIPT_DIR}/stats.json"
stats = []

try:
    with open(stats_fpath) as f:
        stats = json.load(f)
except FileNotFoundError:
    stats = []

while True:
    print("Counting...")
    loc = count_locs_in_path(SCRIPT_DIR)
    stats.append(loc)

    with open(stats_fpath, "w") as f:
        json.dump(stats, f, indent=2)

    pprint(loc)
    time.sleep(COUNT_INTERVAL)