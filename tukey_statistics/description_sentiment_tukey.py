import statsmodels.stats.multicomp as mc

import json
import util.path as path
import pandas as pd


def perform_tukey():
    print('Starting test')
    data = json.load(open(path.data_root() / 'goodreads_sentiment_full.json'))
    emotions = ['Happy', 'Angry', 'Surprise', 'Sad', 'Fear']
    category_map = ['[0-5)', '[5-8)', '[8-12)', '12+']

    dataframe_dict = {}

    type_dict = {'category': 'object', 'sentiment': 'float64'}

    for emotion in emotions:
        dataframe_dict[emotion] = pd.DataFrame(columns=['category', 'sentiment'])
        dataframe_dict[emotion].astype(type_dict)

    for age_category in category_map:
        book_list = data[age_category]
        for book in book_list:
            for emotion_label in emotions:
                sentiment = book['sentiment'][emotion_label]
                dataframe_dict[emotion_label].loc[len(dataframe_dict[emotion_label].index)] = [age_category, sentiment]

    for emotion, dataframe in dataframe_dict.items():
        template = open(path.project_root() / 'tukey_statistics' / 'template.txt').read()

        comp = mc.MultiComparison(dataframe['sentiment'], dataframe['category'])
        post_hoc_res = comp.tukeyhsd()
        summary = post_hoc_res.summary()

        headers = '\t' + ' & '.join(['\\textbf{' + str(item) + '}' for item in summary.data[0]]) + ' \\\\ \\hline \n'
        table_data = ''

        for row in summary.data[1:]:
            table_data += '\t' + ' & '.join([str(item) for item in row]) + ' \\\\ \\hline \n'

        emotion_path = emotion + '.txt'

        full_caption = 'Description ' + emotion.lower() + ' tukey test'

        template = template.replace('{headers}', headers)
        template = template.replace('{data}', table_data)
        template = template.replace('{caption}', full_caption)
        template = template.replace('{styling}', '|ll|llll|l|')

        with open(path.data_root() / 'statistics' / 'description' / emotion_path, 'w') as file:
            file.write(template)
    return dataframe_dict.keys()


perform_tukey()
