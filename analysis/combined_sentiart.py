from util import path

from analysis import senti_art_fulltext
from analysis import senti_art_description

senti_art_fulltext.analyse_book_list_sentiment(path.data_root() / 'wikisource.json')
senti_art_description.analyse_goodreads_sentiment(path.data_root() / 'grouped_goodreads.json')