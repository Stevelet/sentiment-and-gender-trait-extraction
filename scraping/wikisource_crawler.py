from bs4 import BeautifulSoup
from scraping.html_cacher import retrieve_html

url_root = "https://en.wikisource.org"
base_url = url_root + "/wiki/Portal:Children%27s_literature"

soup_str = retrieve_html(base_url)
soup = BeautifulSoup(soup_str, 'html.parser')

print(soup.find_all("span", {"class": "mw-headline"}))