import json
import os

import util.path as path
import util.gender_classifier as gc

directory = path.data_root() / 'description_gender'

pronoun_map = {'he': 'male', 'him': 'male', 'himself': 'male', 'his': 'male', 'she': 'female', 'her': 'female',
               'hers': 'female', 'herself': 'female'}


def breakdown_gender_distribution(file_name, book_collection_path):
    book_collection = json.load(open(book_collection_path, 'r'))

    book_breakdown_collection = []

    for book_details in book_collection:
        name_genders = {}
        book_breakdown = {}
        for name in book_details['names']:
            breakdown = gc.lookup(name)
            name_genders.setdefault(name, {'F': 0, 'M': 0})['F'] += breakdown[0][0]
            name_genders.setdefault(name, {'F': 0, 'M': 0})['M'] += breakdown[0][1]

        book_breakdown['name_genders'] = name_genders

        pronoun_genders = {'male': 0, 'female': 0}

        for pronoun, value in book_details['pronouns'].items():
            pronoun_genders[pronoun_map[pronoun]] += value

        book_breakdown['pronoun_genders'] = pronoun_genders
        book_breakdown['title'] = book_details['book']['title']
        book_breakdown['perspectives'] = book_details['perspectives']
        book_breakdown_collection.append(book_breakdown)

    with open(path.data_root() / 'description_gender_breakdown' / file_name, 'w+') as file:
        st = json.dumps(book_breakdown_collection)
        file.write(st)


for category_file in os.listdir(directory):
    breakdown_gender_distribution(category_file, directory / category_file)
