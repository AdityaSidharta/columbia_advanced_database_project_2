import urllib

import numpy as np
from bs4 import BeautifulSoup
from googleapiclient.discovery import build

NUM_CHARACTER = 20000


def query(client_key, engine_key, query):
    resource = build("customsearch", "v1", developerKey=client_key).cse()
    result = resource.list(q=query, cx=engine_key).execute()
    return [item["link"] for item in result["items"]]


def scrape(idx_site, proposed_site):
    try:
        html = urllib.request.urlopen(proposed_site).read()
        soup = BeautifulSoup(html, "html.parser")
        sentence = soup.get_text(separator=" ")
        assert len(sentence.strip())
        print("")
        print("")
        print("URL ( {} / 10): {}".format(idx_site + 1, proposed_site))
        print("Fetching text from url ...")
        return " ".join(sentence.split())
    except:
        return None


def trim(text_site):
    n_prev = len(text_site)
    words_site = text_site.split()
    n_words = np.array([len(x) for x in words_site])
    cumsum_words = np.cumsum(n_words)
    adder = np.arange(len(words_site))
    assert len(n_words) == len(adder)
    cumsum_full = cumsum_words + adder
    idx = np.max(np.where(cumsum_full < NUM_CHARACTER)) + 1
    trim_site = " ".join(words_site[:idx])
    n_cur = len(trim_site)
    assert n_cur < NUM_CHARACTER
    if n_cur != n_prev:
        print("Trimming webpage content from {} to {} characters".format(n_prev, n_cur))
    return trim_site


def get_query(query, result, previous_queries):
    subjects = []
    objects = []
    confidences = []

    if len(result):
        for key, value in result.items():
            subjects.append(key[0])
            objects.append(key[1])
            confidences.append(value)

        idxs = np.argsort(confidences)[::-1]
        for idx in idxs:
            proposed_query = subjects[idx] + " " + objects[idx]
            if proposed_query not in previous_queries:
                return proposed_query
        return None
    else:
        return query
