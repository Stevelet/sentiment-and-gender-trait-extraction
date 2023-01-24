import tukey_statistics.description_gender_tukey as description_gender
import tukey_statistics.fulltext_gender_tukey as fulltext_gender
import tukey_statistics.description_sentiment_tukey as description_sentiment
import tukey_statistics.fulltext_sentiment_tukey as fulltext_sentiment

from util import path

description_sentiment_tukey = description_sentiment.perform_tukey()
fulltext_sentiment_tukey = fulltext_sentiment.perform_tukey()
description_gender_tukey = description_gender.perform_tukey()
fulltext_gender_tukey = fulltext_gender.perform_tukey()

with open(path.data_root() / 'statistics' / 'combined.txt', 'w') as out_file:
    out_str = ""

    out_str += "\\subsection{Description sentiment traits} \n"

    for file_name in description_sentiment_tukey:
        file_str = file_name + '.txt'
        file_content = open(path.data_root() / 'statistics' / 'description' / file_str, 'r').read()
        out_str += file_content + '\n\n'

    out_str += '\\newpage\n\n'

    out_str += "\\subsection{Fulltext sentiment traits} \n"

    for file_name in fulltext_sentiment_tukey:
        file_str = file_name + '.txt'
        file_content = open(path.data_root() / 'statistics' / 'fulltext' / file_str, 'r').read()
        out_str += file_content + '\n\n'

    out_str += '\\newpage\n\n'

    out_str += "\\subsection{Description gender traits} \n"

    for file_name in description_gender_tukey:
        file_str = file_name.lower().replace(' ', '_') + '.txt'
        file_content = open(path.data_root() / 'statistics' / 'description' / file_str, 'r').read()
        out_str += file_content + '\n\n'

    out_str += '\\newpage\n\n'

    out_str += "\\subsection{Fulltext gender traits} \n"

    for file_name in fulltext_gender_tukey:
        file_str = file_name.lower().replace(' ', '_') + '.txt'
        file_content = open(path.data_root() / 'statistics' / 'fulltext' / file_str, 'r').read()
        out_str += file_content + '\n\n'

    out_str += '\\newpage\n\n'

    out_file.write(out_str)