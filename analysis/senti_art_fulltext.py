import json

import lib.SentiArt.sentiart as sa
from util import path
import math

progress_map = {}

def analyse_chapter_sentiment(chapter_tuple):
    index, chapter = chapter_tuple
    chapter_sentiment_list = sa.apply_sentiart_to_file(chapter)

    chapter_sentiment_dict = {}

    for line in chapter_sentiment_list:
        for key, value in line:
            existing = chapter_sentiment_dict.setdefault(key, (0, 0))
            if not math.isnan(value):
                chapter_sentiment_dict[key] = (existing[0] + 1, existing[1] + value)

    chapter_sentiment = {}

    for key, value in chapter_sentiment_dict.items():
        if value[0] > 0 and value[1] > 0:
            chapter_sentiment[key] = float(value[1]) / float(value[0])
        else:
            chapter_sentiment[key] = 0

    print("#", end='')

    return index, chapter_sentiment


def analyse_book_sentiment(book):
    chapters = book['chapters']
    chapter_sentiments = {}
    for chapter_tuple in enumerate(chapters):
        mapped_chapter_tuple = analyse_chapter_sentiment(chapter_tuple)
        chapter_sentiments[str(mapped_chapter_tuple[0])] = mapped_chapter_tuple[1]
    book['chapter_sentiments'] = chapter_sentiments
    return book


def analyse_book_list_sentiment(book_list_path):
    with open(book_list_path, 'r') as file:
        book_list = json.load(file)

    age_map = {}
    book_count = len(book_list)
    done_count = 0
    print('Starting fulltext book analysis on ' + str(book_count) + ' books')
    for mapped_book in map(analyse_book_sentiment, book_list):
        if mapped_book['recommended_age'] not in age_map:
            age_map[mapped_book['recommended_age']] = []
        age_map[mapped_book['recommended_age']].append(mapped_book)
        done_count += 1
        print('\nFinished (' + str(done_count) + '/' + str(book_count) + ')')

    with open(path.data_root() / 'wikisource_sentiart_sentiment.json', 'w') as file:
        file.write(json.dumps(age_map))


analyse_book_list_sentiment(path.data_root() / 'wikisource.json')
