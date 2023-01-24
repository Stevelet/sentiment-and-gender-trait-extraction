import json
import os

import pandas as pd
import seaborn as sns
import util.path as path

category_map = {'0+': '[0-5)', '3+': '[0-5)', '5+': '[5-8)', '8+': '[8-12)', '12+': '12+'}
category_list = ['[0-5)', '[5-8)', '[8-12)', '12+']


def assemble_gender_collection():
    gender_paths = os.listdir(path.data_root() / 'gender')

    collection_dict_inner = {}

    for gender_path in gender_paths:
        book_dict = {}
        gender_dict = json.loads(open(path.data_root() / 'gender' / gender_path, 'r').read())
        breakdown_dict = json.loads(open(path.data_root() / 'gender_breakdown' / gender_path, 'r').read())

        age_category = category_map[gender_dict['recommended_age']]

        third_person_male = breakdown_dict['pronoun_genders']['male']
        third_person_female = breakdown_dict['pronoun_genders']['female']

        book_dict['Third person male'] = [third_person_male, 'Third person male', age_category]
        book_dict['Third person female'] = [third_person_female, 'Third person female', age_category]

        male_names = 0
        female_names = 0

        for name, genders in breakdown_dict['name_genders'].items():
            male_names += genders['M']
            female_names += genders['F']

        book_dict['Male names'] = [male_names, 'Male names', age_category]
        book_dict['Female names'] = [female_names, 'Female names', age_category]

        perspective_dicts = gender_dict['perspective_words']

        first_person_words = 0
        second_person_words = 0

        for _, perspective_words in perspective_dicts.items():
            first_person_words += perspective_words['i'] + perspective_words['me'] + perspective_words['we'] + \
                                  perspective_words['us']
            second_person_words += perspective_words['you'] + perspective_words['they']

        book_dict['First person words'] = [first_person_words, 'First person words', age_category]
        book_dict['Second person words'] = [second_person_words, 'Second person words', age_category]

        t = third_person_female + third_person_male + male_names + female_names + first_person_words + second_person_words

        collection_dict_inner.setdefault(age_category, []).append((t, book_dict))
    return collection_dict_inner


sentiment_frame = pd.DataFrame(columns=['Count', 'Perspective Label', 'Age Category'])

collection_dict = assemble_gender_collection()

for category in category_list:
    for total, b_dict in collection_dict[category]:
        for key, value in b_dict.items():
            if value[0] > 0.0:
                sentiment_frame.loc[len(sentiment_frame.index)] = [float(value[0]) / float(total), value[1], value[2]]
            else:
                sentiment_frame.loc[len(sentiment_frame.index)] = value

sentiment_frame.sort_values(by=['Age Category'])

plot = sns.boxplot(x=sentiment_frame['Age Category'],
                   y=sentiment_frame['Count'],
                   hue=sentiment_frame['Perspective Label'])

plot.figure.savefig(path.data_root() / 'fulltext_gender.png')
