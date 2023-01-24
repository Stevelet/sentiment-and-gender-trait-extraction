import json

import nltk

from util import path
from multiprocessing import pool
import text2emotion as te
import random
import time

nltk.download('omw-1.4')
threadpool = pool.ThreadPool()


def analyse_description_sentiment(book):
    description_sentiment = None
    success = False
    slept_for = 1
    while success is not True:
        try:
            description_sentiment = te.get_emotion(book['description'])
            success = True
        except:
            time.sleep(slept_for)
            slept_for += 1
            if slept_for > 60:
                print(slept_for)
    print("#", end='')

    return book, description_sentiment



def analyse_goodreads_sentiment(file, n_per_category=None):
    grouped_goodreads = json.loads(open(file, 'r').read())
    sentiment_dict = {}

    for category, book_list in grouped_goodreads.items():
        print('\nStarting category : ', category)
        if n_per_category is not None:
            sample = random.sample(book_list, n_per_category)
        else:
            sample = book_list

        for book, sentiment in threadpool.imap_unordered(analyse_description_sentiment, sample):
            print('#', end='')
            book['sentiment'] = sentiment
            sentiment_dict.setdefault(category, []).append(book)

    with open(path.data_root() / 'goodreads_sentiment_full.json', 'w') as file:
        file.write(json.dumps(sentiment_dict))


analyse_goodreads_sentiment(path.data_root() / 'grouped_goodreads.json')
