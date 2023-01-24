from util import path
import json

category_map = {'0+': '[0-5)', '3+': '[0-5)', '5+': '[5-8)', '8+': '[8-12)', '12+': '12+'}

wikisource_list = json.loads(open(path.data_root() / 'wikisource.json', 'r').read())
goodreads_dict = json.loads(open(path.data_root() / 'grouped_goodreads.json', 'r').read())

wikisource_buckets = {key: 0 for key in category_map.values()}
goodreads_buckets = {key: 0 for key in category_map.values()}

for item in wikisource_list:
    wikisource_buckets[category_map[item['recommended_age']]] += 1

for key, item in goodreads_dict.items():
    goodreads_buckets[key] += len(item)