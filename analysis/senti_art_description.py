import json

import random
import lib.SentiArt.sentiart as sa
from util import path
import math

def analyse_description_sentiment(book):
    description_sentiment_list = sa.apply_sentiart_to_text(book['description'])

    description_sentiment_dict = {}

    for line in description_sentiment_list:
        for key, value in line:
            existing = description_sentiment_dict.setdefault(key, (0, 0))
            if not math.isnan(value):
                description_sentiment_dict[key] = (existing[0] + 1, existing[1] + value)

    description_sentiment = {}

    for key, value in description_sentiment_dict.items():
        if value[0] > 0 and value[1] > 0:
            description_sentiment[key] = float(value[1]) / float(value[0])
        else:
            description_sentiment[key] = 0

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

        book_count = len(sample)
        done_count = 0
        for book, sentiment in map(analyse_description_sentiment, sample):
            book['sentiment'] = sentiment
            sentiment_dict.setdefault(category, []).append(book)
            print('\nFinished (' + str(done_count) + '/' + str(book_count) + ')')

    with open(path.data_root() / 'goodreads_sentiart_sentiment_full.json', 'w') as file:
        file.write(json.dumps(sentiment_dict))


analyse_goodreads_sentiment(path.data_root() / 'grouped_goodreads.json')