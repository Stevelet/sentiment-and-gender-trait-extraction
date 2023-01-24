import statsmodels.stats.multicomp as mc

import json
import util.path as path
import pandas as pd


def perform_text2emotion_tukey(emotion_map):
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
        grouping_map = {}

        comp = mc.MultiComparison(dataframe['sentiment'], dataframe['category'])
        post_hoc_res = comp.tukeyhsd()
        summary = post_hoc_res.summary()

        for row in summary.data[1:]:
            group_key = tuple(sorted([row[0], row[1]]))
            data = row[2:]
            grouping_map[group_key] = (summary.data[0], data, None)

        emotion_map[emotion] = grouping_map
    return emotion_map, dataframe_dict.keys()


def perform_sentiart_tukey(emotion_map):
    data = json.load(open(path.data_root() / 'goodreads_sentiart_sentiment_full.json'))
    emotions = {'Happy': 'hap_z', 'Angry': 'ang_z', 'Surprise': 'surp_z', 'Sad': 'sad_z', 'Fear': 'fear_z'}
    category_map = ['[0-5)', '[5-8)', '[8-12)', '12+']

    dataframe_dict = {}

    type_dict = {'category': 'object', 'sentiment': 'float64'}

    for emotion in emotions.keys():
        dataframe_dict[emotion] = pd.DataFrame(columns=['category', 'sentiment'])
        dataframe_dict[emotion].astype(type_dict)

    for age_category in category_map:
        book_list = data[age_category]
        for book in book_list:
            for emotion_label, emotion_key in emotions.items():
                sentiment = book['sentiment'][emotion_key]
                dataframe_dict[emotion_label].loc[len(dataframe_dict[emotion_label].index)] = [age_category, sentiment]

    for emotion, dataframe in dataframe_dict.items():
        grouping_map = emotion_map[emotion]

        comp = mc.MultiComparison(dataframe['sentiment'], dataframe['category'])
        post_hoc_res = comp.tukeyhsd()
        summary = post_hoc_res.summary()

        for row in summary.data[1:]:
            group_key = tuple(sorted([row[0], row[1]]))
            data = row[2:]
            grouping_map[group_key] = (grouping_map[group_key][0], grouping_map[group_key][1], data)

        emotion_map[emotion] = grouping_map
    return emotion_map, dataframe_dict.keys()


def perform_tukey():
    emotion_map = {}
    print('Starting test')
    emotion_map, emotion_keys_text2emotion = perform_text2emotion_tukey(emotion_map)
    emotion_map, emotion_keys_sentiart = perform_sentiart_tukey(emotion_map)

    assert tuple(emotion_keys_text2emotion) == tuple(emotion_keys_sentiart)

    headers = ""
    table_data = ""
    for emotion, row_map in emotion_map.items():
        template = open(path.project_root() / 'tukey_statistics' / 'template.txt').read()
        for grouping, row in row_map.items():
            headers = '\t'
            headers += ' & '.join(['\\textbf{' + str(item) + '}' for item in row[0]]) + ' & '
            headers += ' & '.join(['\\textbf{' + str(item) + '}' for item in row[0][2:]])
            headers += ' \\\\ \\hline \n'

            table_data += '\t' + ' & '.join(grouping) + ' & '
            table_data += ' & '.join([str(item) for item in row[1]]) + ' & '
            table_data += ' & '.join([str(item) for item in row[2]])
            table_data += ' \\\\ \\hline \n'

        emotion_path = emotion + '.txt'

        full_caption = 'Description ' + emotion.lower() + ' tukey test'

        template = template.replace('{headers}', headers)
        template = template.replace('{data}', table_data)
        template = template.replace('{caption}', full_caption)
        template = template.replace('{styling}', '|ll|llll|l|llll|l|')

        with open(path.data_root() / 'statistics' / 'description' / emotion_path, 'w') as file:
            file.write(template)
    return emotion_keys_text2emotion

perform_tukey()