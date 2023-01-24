import json
import os
from functools import reduce
import util.path as path
import util.name_classifier as name_classifier
import time
from util.dict_util import merge_dictionary

basic_pronouns = ['he', 'him', 'himself', 'his', 'she', 'her', 'hers', 'herself']
perspective_options = ['i', 'me', 'you', 'they', 'we', 'us']


# Dictionary source: https://github.com/dwyl/english-words

def analyse_line_names(line):
    words = ' '.join(filter(lambda word: word.isalpha(), line.split(' ')))

    return [name[0] for name in name_classifier.extract_person_names(words)]


def analyse_line_pronouns(line):
    words = filter(lambda w: w.isalpha(), line.split(' '))

    pronoun_map = {key: 0 for key in basic_pronouns}

    for word in words:
        low = word.lower()
        if low in basic_pronouns:
            pronoun_map[low] += 1

    return pronoun_map


def analyse_line_perspective(line):
    words = filter(lambda w: w.isalpha(), line.split(' '))

    perspective_map = {key: 0 for key in perspective_options}

    for word in words:
        low = word.lower()
        if low in perspective_options:
            perspective_map[low] += 1

    return perspective_map


def analyse_description_names_and_pronouns(book):
    lines = book['description'].split('\n')

    names = [item for sublist in list(map(analyse_line_names, lines)) for item in sublist]
    pronouns = reduce(merge_dictionary, list(map(analyse_line_pronouns, lines)))
    perspectives = reduce(merge_dictionary, list(map(analyse_line_perspective, lines)))

    return names, pronouns, perspectives


def analyse_description_list_names_and_pronouns(book_list_path):
    dir_name = path.data_root() / 'description_gender'
    with open(book_list_path, 'r', encoding='utf-8') as file:
        book_dict = json.load(file)

    for category, book_list in book_dict.items():
        file_name = category + '.json'
        gendered_list = []

        if os.path.exists(dir_name / file_name):
            continue

        print('\nStarting with category : ', category)
        for book in book_list:
            names, pronouns, perspectives = analyse_description_names_and_pronouns(book)
            gendered_list.append({'book': book, 'names': names, 'pronouns': pronouns, 'perspectives': perspectives})
            print('#', end='')

        with open(dir_name / file_name, 'w', encoding='utf-8') as file:
            file.write(json.dumps(gendered_list))


analyse_description_list_names_and_pronouns(path.data_root() / 'grouped_goodreads.json')
