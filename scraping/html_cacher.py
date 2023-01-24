from urllib.request import urlopen
from util.path import data_root
import re
import os

def sanitize_url(url):
    return re.sub('[^0-9a-zA-Z]+', '_', url)

def get_or_create_dir():
    dir_path = data_root() / 'html_cache'
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    return dir_path

def retrieve_html(url):
    """
    Retrieve the html found at the given url and parse to string.

    :param url: Url to GET
    :return: The body html as a string
    """
    file_path = sanitize_url(url) + '.txt'
    dir_path = get_or_create_dir()
    combined = dir_path / file_path

    if os.path.exists(combined):
        return open(combined, 'r+', encoding="utf-8").read()
    else:
        with urlopen(url) as response:
            html = response.read()
            response.close()
            html_str = str(html.decode('utf-8'))

            open(combined, 'w+', encoding="utf-8").write(html_str)

            return html_str