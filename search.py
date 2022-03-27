from googleapiclient.discovery import build
import urllib
from bs4 import BeautifulSoup
import numpy as np


NUM_CHARACTER = 20000

def query(client_key, engine_key, query):
    resource = build("customsearch", "v1", developerKey=client_key).cse()
    result = resource.list(q=query, cx=engine_key).execute()
    return [item['link'] for item in result["items"]]

def scrape(proposed_site):
    try:
        html = urllib.request.urlopen(proposed_site).read()
        soup = BeautifulSoup(html, 'html.parser')
        sentence = soup.get_text(separator = " ")
        return ' '.join(sentence.split())
    except ValueError:
        return None

def trim(text_site):
    words_site = text_site.split()
    n_words = np.array([len(x) for x in words_site])
    cumsum_words = np.cumsum(n_words)
    adder = np.arange(len(words_site))
    assert len(n_words) == len(adder)
    cumsum_full = cumsum_words + adder
    idx = np.max(np.where(cumsum_full < NUM_CHARACTER)) + 1
    trim_site = ' '.join(words_site[idx])
    assert len(trim_site) < NUM_CHARACTER
    return trim_site

