from util import path
import pandas as pd
import json
import os

files = os.listdir(path.data_root() / 'gender_breakdown')
name_list = []

for file_name in files:
    breakdown = json.loads(open(path.data_root() / 'gender_breakdown' / file_name).read())
    name_genders = breakdown['name_genders']

    for name, gender_breakdown in name_genders.items():
        name_list.append((name, tuple(gender_breakdown.values())))
        if name == 'Samarcand':
            print(file_name)
            print(gender_breakdown)

sorted_name_list = list(sorted(name_list, key=lambda i: abs(i[1][0] - i[1][1])))