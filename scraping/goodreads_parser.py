import json
import csv

from util.path import data_root

goodreads_dicts = open(data_root() / 'goodreads.json').read().split('\n')

parsed_list = []
for d in goodreads_dicts:
    try:
        parsed = json.loads(d)
        parsed_list.append(parsed)
        print('#', end='')
    except:
        print('Skipped')
parsed_str = json.dumps(parsed_list)

with open(data_root() / 'parsed_goodreads.json', 'w') as file:
    file.write(parsed_str)
