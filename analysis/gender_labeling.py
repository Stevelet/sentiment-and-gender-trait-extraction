import json
import os

import util.path as path
import numpy as np
import matplotlib.pyplot as plt
from functools import reduce
from util.dict_util import merge_dictionary
import util.gender_classifier as gc

directory = path.data_root() / 'gender'

pronoun_map = {'he': 'male', 'him': 'male', 'himself': 'male', 'his': 'male', 'she': 'female', 'her': 'female',
               'hers': 'female', 'herself': 'female'}


def breakdown_gender_distribution(book_path):
    book = json.load(open(book_path, 'r'))

    name_genders = {}

    for key in book['chapter_person_names'].keys():
        chapter_names = book['chapter_person_names'][key]
        for name in chapter_names:
            breakdown = gc.lookup(name)
            name_genders.setdefault(name, {'F': 0, 'M': 0})['F'] += breakdown[0][0]
            name_genders.setdefault(name, {'F': 0, 'M': 0})['M'] += breakdown[0][1]

    pronoun_genders = {'male': 0, 'female': 0}

    for chapter, values in book['chapter_pronouns'].items():
        for key, value in values.items():
            pronoun_genders[pronoun_map[key]] += value

    file_name = path.make_path_safe(book['title']) + '.json'
    with open(path.data_root() / 'gender_breakdown' / file_name, 'w+') as file:
        st = json.dumps({'title': book['title'], 'pronoun_genders': pronoun_genders, 'name_genders': name_genders})
        file.write(st)


for book_file in os.listdir(directory):
    breakdown_gender_distribution(directory / book_file)
