from util import path
import json

wikisource = json.loads(open(path.data_root() / 'wikisource.json', 'r').read())
goodreads = json.loads(open(path.data_root() / 'grouped_goodreads.json', 'r').read())

wikisource_year = 0
wikisource_count = 0

goodreads_year = 0
goodreads_count = 0

for item in wikisource:
    if 'publishing_year' in item.keys():
        if item['publishing_year'] != '':
            wikisource_year += int(item['publishing_year'])
            wikisource_count += 1

for age_group, li in goodreads.items():
    for item in li:
        if 'publication_year' in item.keys():
            if item['publication_year'] != '':
                goodreads_year += int(item['publication_year'])
                goodreads_count += 1

print("Wikisource average year : " + str(wikisource_year / wikisource_count))
print("Goodreads average year : " + str(goodreads_year / goodreads_count))