import json
import re
from multiprocessing import pool

from util.path import data_root

goodreads_list = json.load(open(data_root() / 'parsed_goodreads.json'))
print('Loaded json file')

threadpool = pool.ThreadPool()

category_list = ['[0-5)', '[5-8)', '[8-12)', '12+']
age_ranges = list(enumerate([set(list(range(0, 5))), set(list(range(5, 8))), set(list(range(8, 12))), set(list(range(12, 101)))]))

age_dict = {}
print("Processing ", len(goodreads_list))


def process_item(item):
    if not len(item['description']) > 0:
        return None, None

    shelves = item['popular_shelves']
    age_result = None
    yr_result = None
    for shelve in shelves:
        name = shelve['name']
        if age_result is None:
            age_result = re.search('ages-([0-9]+)-?t?o?-?([0-9]+)?', name)
        if yr_result is None:
            yr_result = re.search('yr-([0-9]+)-?a?g?e?-?([0-9]+)?', name)
    return_tuple = (0, (None, None))
    if age_result is not None and len(age_result.groups()) > 0:
        if age_result.group(2) is None:
            current_range = {int(age_result.group(1))}
        else:
            current_range = set(list(range(int(age_result.group(1)), int(age_result.group(2)))))

        for index, cat_range in age_ranges:
            sect = cat_range.intersection(current_range)
            if len(sect) > return_tuple[0]:
                return_tuple = (len(sect), (index, item))
    if yr_result is not None and len(yr_result.groups()) > 0:
        if yr_result.group(2) is None:
            current_range = {int(yr_result.group(1))}
        else:
            current_range = set(list(range(int(yr_result.group(1)), int(yr_result.group(2)))))

        for index, cat_range in age_ranges:
            sect = cat_range.intersection(current_range)
            if len(sect) > return_tuple[0]:
                return_tuple = (len(sect), (index, item))

    return return_tuple[1]


for cat_index, book_option in threadpool.imap_unordered(process_item, goodreads_list):
    if book_option is not None:
        age_dict.setdefault(category_list[cat_index], []).append(book_option)

print(age_dict)

with open(data_root() / 'grouped_goodreads.json', 'w') as file:
    file.write(json.dumps(age_dict))
