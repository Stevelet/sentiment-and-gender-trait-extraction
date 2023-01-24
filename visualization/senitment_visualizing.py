import json
import util.path as path
import functools as t
import seaborn as sns
import pandas as pd

data = json.load(open(path.data_root() / 'wikisource_sentiment.json'))
emotions = ['Happy', 'Angry', 'Surprise', 'Sad', 'Fear']
emotion_colors = ['green', 'red', 'yellow', 'blue', 'orange']
category_map = {0: '[0-5)', 3: '[0-5)', 5: '[5-8)', 8: '[8-12)', 12: '12+'}

keys = sorted([int(key.replace('+', '')) for key in list(data.keys())])
plot_data = []
average_dict = {}
for i in range(len(keys)):
    key = keys[i]
    raw_key = str(key) + '+'

    sentiments = [list(item['chapter_sentiments'].values()) for item in data[raw_key]]
    unpacked_book_sentiments = [[[chapter[emotion] for emotion in emotions] for chapter in book] for book in sentiments]
    filtered_book_sentiments = list(filter(lambda b: len(b) > 0,
                                           [[chapter for chapter in book if sum(chapter) > 0] for book in
                                            unpacked_book_sentiments]))
    total_book_sentiment = [(len(book), t.reduce(lambda l, r: list(map(lambda l1, r1: l1 + r1, l, r)), book)) for book
                            in filtered_book_sentiments]
    average_book_sentiment = [list(map(lambda chapter: chapter / float(book[0]), book[1])) for book in
                              total_book_sentiment]
    average_dict[key] = average_book_sentiment
    average_category_sentiment = t.reduce(
        lambda l, r: list(map(lambda l1, r1: l1 + r1 / len(average_book_sentiment), l, r)), average_book_sentiment)
    plot_data.append(average_category_sentiment)

sentiment_frame = pd.DataFrame(columns=['Sentiment', 'Emotion Label', 'Age Category'])

for category_key, sentiment_list in average_dict.items():
    for sentiment_tuple in sentiment_list:
        for index, sentiment_value in enumerate(sentiment_tuple):
            emotion_label = emotions[index]
            sentiment = sentiment_value
            age_category = category_map[category_key]
            if not sentiment > 0.5:
                sentiment_frame.loc[len(sentiment_frame.index)] = [sentiment, emotion_label, age_category]

print(sentiment_frame)

plot = sns.boxplot(x=sentiment_frame['Age Category'],
                   y=sentiment_frame['Sentiment'],
                   hue=sentiment_frame['Emotion Label'])

plot.figure.savefig(path.data_root() / 'fulltext_sentiment.png')
