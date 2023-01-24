import statsmodels.stats.multicomp as mc

from visualization import description_gender_visualization
import pandas as pd

from util import path

def perform_tukey():
    collection_dict = description_gender_visualization.assemble_gender_collection()

    dataframe_dict = {}

    for category, book_list in collection_dict.items():
        for total, book_dict in book_list:
            for key, item_array in book_dict.items():
                dataframe = dataframe_dict.setdefault(item_array[1], pd.DataFrame(columns=['category', 'value']))
                if item_array[0] > 0:
                    dataframe.loc[len(dataframe)] = [category, float(item_array[0]) / total]
                else:
                    dataframe.loc[len(dataframe)] = [category, item_array[0]]

    for perspective, dataframe in dataframe_dict.items():
        template = open(path.project_root() / 'tukey_statistics' / 'template.txt').read()

        comp = mc.MultiComparison(dataframe['value'], dataframe['category'])
        post_hoc_res = comp.tukeyhsd()
        summary = post_hoc_res.summary()

        perspective_path = perspective.lower().replace(' ', '_') + '.txt'

        headers = '\t' + ' & '.join(['\\textbf{' + str(item) + '}' for item in summary.data[0]]) + ' \\\\ \\hline \n'
        table_data = ''
        full_caption = 'Description ' + perspective.lower() + ' tukey test'

        for row in summary.data[1:]:
            table_data += '\t' + ' & '.join([str(item) for item in row]) + ' \\\\ \\hline \n'

        template = template.replace('{headers}', headers)
        template = template.replace('{data}', table_data)
        template = template.replace('{caption}', full_caption)
        template = template.replace('{styling}', '|ll|llll|l|')

        with open(path.data_root() / 'statistics' / 'description' / perspective_path, 'w') as file:
            file.write(template)
    return dataframe_dict.keys()