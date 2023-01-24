import json
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import util.path as path

category_map = {'0+': '[0-5)', '3+': '[0-5)', '5+': '[5-8)', '8+': '[8-12)', '12+': '12+'}
category_list = ['[0-5)', '[5-8)', '[8-12)', '12+']

gender_paths = os.listdir(path.data_root() / 'gender')


def assemble_gender_collection():
    collection_dict_local = {}

    for category in category_list:
        file_name = category + '.json'
        gender_list = json.loads(open(path.data_root() / 'description_gender' / file_name, 'r').read())
        gender_breakdown_list = json.loads(
            open(path.data_root() / 'description_gender_breakdown' / file_name, 'r').read())

        zipped = zip(gender_list, gender_breakdown_list)

        for gender_dict, breakdown_dict in zipped:
            book_dict = {}
            perspective_words = gender_dict['perspectives']

            first_person_words = perspective_words['i'] + perspective_words['me'] + perspective_words['we'] + \
                                 perspective_words['us']
            second_person_words = perspective_words['you'] + perspective_words['they']

            book_dict['First person words'] = [first_person_words, 'First person words', category]
            book_dict['Second person words'] = [second_person_words, 'Second person words', category]

            third_person_male = breakdown_dict['pronoun_genders']['male']
            third_person_female = breakdown_dict['pronoun_genders']['female']

            book_dict['Third person male'] = [third_person_male, 'Third person male', category]
            book_dict['Third person female'] = [third_person_female, 'Third person female', category]

            male_names = 0
            female_names = 0

            for name, name_genders in breakdown_dict['name_genders'].items():
                male_names += name_genders['M']
                female_names += name_genders['F']

            t = first_person_words + second_person_words + third_person_male + third_person_female + male_names + female_names

            book_dict['Male names'] = [male_names, 'Male names', category]
            book_dict['Female names'] = [female_names, 'Female names', category]

            collection_dict_local.setdefault(category, []).append((t, book_dict))
    return collection_dict_local


collection_dict = assemble_gender_collection()

sentiment_frame = pd.DataFrame(columns=['Count', 'Perspective Label', 'Age Category'])

for cat in category_list:
    for total, b_dict in collection_dict[cat]:
        for key, value in b_dict.items():
            if value[0] > 0.0:
                sentiment_frame.loc[len(sentiment_frame.index)] = [float(value[0]) / float(total), value[1], value[2]]
            else:
                sentiment_frame.loc[len(sentiment_frame.index)] = value

plot = sns.boxplot(x=sentiment_frame['Age Category'],
                   y=sentiment_frame['Count'],
                   hue=sentiment_frame['Perspective Label'])

plot.figure.savefig(path.data_root() / 'description_gender.png')
