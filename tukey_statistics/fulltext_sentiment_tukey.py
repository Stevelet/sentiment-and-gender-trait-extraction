import statsmodels.stats.multicomp as mc

import json
import util.path as path
import pandas as pd

def perform_tukey():
    data = json.load(open(path.data_root() / 'wikisource_sentiment.json'))
    emotions = ['Happy', 'Angry', 'Surprise', 'Sad', 'Fear']
    emotion_colors = ['green', 'red', 'yellow', 'blue', 'orange']
    category_map = {'0+': '[0-5)', '3+': '[0-5)', '5+': '[5-8)', '8+': '[8-12)', '12+': '12+'}

    dataframe_dict = {}

    type_dict = {'category': 'object', 'sentiment': 'float64'}


    for emotion in emotions:
        dataframe_dict[emotion] = pd.DataFrame(columns=['category', 'sentiment'])
        dataframe_dict[emotion].astype(type_dict)

    for age_key, age_category in category_map.items():
        book_list = data[age_key]
        for book in book_list:
            sentiment_dict = {key: 0 for key in emotions}
            for chapter_sentiment in book['chapter_sentiments'].values():
                for sentiment_key, value in chapter_sentiment.items():
                    sentiment_dict[sentiment_key] += value

            for emotion_label in emotions:
                sentiment = sentiment_dict[emotion_label] / float(len(book['chapter_sentiments']))
                dataframe_dict[emotion_label].loc[len(dataframe_dict[emotion_label].index)] = [age_category, sentiment]

    for emotion, dataframe in dataframe_dict.items():
        template = open(path.project_root() / 'tukey_statistics' / 'template.txt').read()

        comp = mc.MultiComparison(dataframe['sentiment'], dataframe['category'])
        post_hoc_res = comp.tukeyhsd()
        summary = post_hoc_res.summary()

        emotion_path = emotion + '.txt'

        headers = '\t' + ' & '.join(['\\textbf{' + str(item) + '}' for item in summary.data[0]]) + ' \\\\ \\hline \n'
        table_data = ''
        full_caption = 'Fulltext ' + emotion.lower() + ' tukey test'

        for row in summary.data[1:]:
            table_data += '\t' + ' & '.join([str(item) for item in row]) + ' \\\\ \\hline \n'

        template = template.replace('{headers}', headers)
        template = template.replace('{data}', table_data)
        template = template.replace('{caption}', full_caption)
        template = template.replace('{styling}', '|ll|llll|l|')

        with open(path.data_root() / 'statistics' / 'fulltext' / emotion_path, 'w') as file:
            file.write(template)
    return dataframe_dict.keys()