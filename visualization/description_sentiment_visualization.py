import json
import util.path as path
import functools as t
import seaborn as sns
import pandas as pd

data = json.load(open(path.data_root() / 'goodreads_sentiment_full.json'))
emotions = ['Happy', 'Angry', 'Surprise', 'Sad', 'Fear']
emotion_colors = ['green', 'red', 'yellow', 'blue', 'orange']
category_map = ['[0-5)', '[5-8)', '[8-12)', '12+']

sentiment_frame = pd.DataFrame(columns=['Sentiment', 'Emotion Label', 'Age Category'])

for age_category in category_map:
    book_list = data[age_category]
    for book in book_list:
        for emotion_label in emotions:
            sentiment = book['sentiment'][emotion_label]
            sentiment_frame.loc[len(sentiment_frame.index)] = [sentiment, emotion_label, age_category]


print(sentiment_frame)

plot = sns.boxplot(x=sentiment_frame['Age Category'],
                   y=sentiment_frame['Sentiment'],
                   hue=sentiment_frame['Emotion Label'])

plot.figure.savefig(path.data_root() / 'goodreads_sentiment.png')
