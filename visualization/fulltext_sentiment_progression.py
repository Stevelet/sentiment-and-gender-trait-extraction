import json

import numpy

import util.path as path
import functools as t
from numpy import arange
from pandas import read_csv
from scipy.optimize import curve_fit
from matplotlib import pyplot
import random


# define the true objective function
def objective(x, a, b, c, d, e, f):
    return (a * x) + (b * x ** 2) + (c * x ** 3) + (d * x ** 4) + (e * x ** 5) + f


# # choose the input and output variables
# x = numpy.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
# y = numpy.array([random.random() for i in range(0, 9)])


data = json.load(open(path.data_root() / 'wikisource_sentiment.json'))
emotions = ['Happy', 'Angry', 'Surprise', 'Sad', 'Fear']
emotion_colors = ['green', 'red', 'yellow', 'blue', 'orange']
category_map = {0: '[0-5)', 3: '[0-5)', 5: '[5-8)', 8: '[8-12)', 12: '12+'}

keys = sorted([int(key.replace('+', '')) for key in list(data.keys())])
plot_data = []
most_key = None
most_list = []
most_count = 0
for i in range(len(keys)):
    key = keys[i]
    raw_key = str(key) + '+'

    sentiments = [list(item['chapter_sentiments'].values()) for item in data[raw_key]]
    unpacked_book_sentiments = [[[chapter[emotion] for emotion in emotions] for chapter in book] for book in sentiments]
    filtered_book_sentiments = list(filter(lambda b: len(b) > 0,
                                           [[chapter for chapter in book if sum(chapter) > 0] for book in
                                            unpacked_book_sentiments]))
    len_mapped_book_sentiment = [(len(book), book) for book in unpacked_book_sentiments]
    multi_chapter_books = list(filter(lambda b: b[0] >= 3, len_mapped_book_sentiment))
    if len(multi_chapter_books) > most_count:
        most_count = len(multi_chapter_books)
        most_key = category_map[key]
        most_list = multi_chapter_books

max_chapter_count = 100

for index, emotion in enumerate(emotions):
    print(index)

    x_list = []
    y_list = []
    for chapter_count, book in most_list:
        for chapter_index, sentiment_list in enumerate(book):
            x_index = (float(chapter_index) / float(chapter_count - 1)) * float(max_chapter_count - 1)
            y_index = sentiment_list[index]

            x_list.append(x_index)
            y_list.append(y_index)

    x = numpy.array(x_list)
    y = numpy.array(y_list)
    s = list((0.5,) * len(x_list))

    # curve fit
    popt, _ = curve_fit(objective, x, y)
    # summarize the parameter values
    a, b, c, d, e, f = popt
    # plot input vs output
    # pyplot.scatter(x, y, s, color=emotion_colors[index])
    # define a sequence of inputs between the smallest and largest known inputs
    x_line = arange(min(x), max(x), 1)
    # calculate the output for the range
    y_line = objective(x_line, a, b, c, d, e, f)
    # create a line plot for the mapping function
    pyplot.plot(x_line, y_line, '--', color=emotion_colors[index])
pyplot.legend(emotions, loc='upper center')
pyplot.ylabel('Sentiment Value')
pyplot.xlabel('Book Percentage')
pyplot.savefig(path.data_root() / 'sentiment_progression.png')