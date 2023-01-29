import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from util import path
import json
import functools as t

emotion_map = {'hap_z': 'Happy', 'ang_z': 'Angry', 'surp_z': 'Surprise', 'sad_z': 'Sad', 'fear_z': 'Fear'}
category_map = {'0+': '[0-5)', '3+': '[0-5)', '5+': '[5-8)', '8+': '[8-12)', '12+': '12+'}
compound_list = []

label_list = []

for key in emotion_map.values():
    label_list.append('Text2Emotion ' + key)

for key in emotion_map.values():
    label_list.append('SentiArt ' + key)

senti_art_description_dict = json.loads(open(path.data_root() / 'goodreads_sentiart_sentiment_full.json').read())
senti_art_fulltext_dict = json.loads(open(path.data_root() / 'wikisource_sentiart_sentiment.json').read())

text2emotion_description_dict = json.loads(open(path.data_root() / 'goodreads_sentiment_full.json').read())
text2emotion_fulltext_dict = json.loads(open(path.data_root() / 'wikisource_sentiment.json').read())

for category_key, category in category_map.items():
    sub_dict = {}

    senti_art_fulltext_subdict = senti_art_fulltext_dict[category_key]
    text2emotion_fulltext_subdict = text2emotion_fulltext_dict[category_key]

    for book in senti_art_fulltext_subdict:
        title = book['title']
        try:
            unpacked = [[chapter[emotion] for emotion in emotion_map.keys()] for chapter in
                        book['chapter_sentiments'].values()]
            sub_total = (len(unpacked), t.reduce(lambda l, r: list(map(lambda l1, r1: l1 + r1, l, r)), unpacked))
            total = list(map(lambda e: e / sub_total[0], sub_total[1]))
            sub_dict.setdefault(title, (None, total))
        except:
            sub_dict.setdefault(title, (None, None))

    for book in text2emotion_fulltext_subdict:
        title = book['title']
        unpacked = [[chapter[emotion] for emotion in emotion_map.values()] for chapter in
                    book['chapter_sentiments'].values()]
        sub_total = (len(unpacked), t.reduce(lambda l, r: list(map(lambda l1, r1: l1 + r1, l, r)), unpacked))
        total = list(map(lambda e: e / sub_total[0], sub_total[1]))
        previous = sub_dict[title]
        sub_dict[title] = (total, previous[1])

    for value in sub_dict.values():
        if value[0] is not None and value[1] is not None:
            compound_list.append(list(value[0]) + list(value[1]))

for category_key, category in category_map.items():
    sub_dict = {}

    senti_art_description_subdict = senti_art_description_dict[category]
    text2emotion_description_subdict = text2emotion_description_dict[category]

    for book in senti_art_description_subdict:
        title = book['title']
        sentiment = book['sentiment']

        sentiments = []
        for key in emotion_map.keys():
            sentiments.append(sentiment[key])

        sub_dict[title] = (None, sentiments)

    for book in text2emotion_description_subdict:
        title = book['title']
        sentiment = book['sentiment']

        if title in sub_dict.keys():
            previous = sub_dict[title]
            sub_dict[title] = (list(sentiment.values()), previous[1])

    for value in sub_dict.values():
        if value[0] is not None and value[1] is not None:
            compound_list.append(list(value[0]) + list(value[1]))

df = pd.DataFrame(data=compound_list, columns=label_list)
corr = df.corr()

fig, ax = plt.subplots(figsize=(15, 15))
plot = sns.heatmap(corr,
                   annot=True,
                   xticklabels=corr.columns.values,
                   yticklabels=corr.columns.values,
                   ax=ax)

plot.figure.savefig(path.data_root() / 'tool_correlation.png')
