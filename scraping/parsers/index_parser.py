from html.parser import HTMLParser
from scraping.parsers.author_parser import AuthorParser
from bs4 import BeautifulSoup
from scraping.html_cacher import retrieve_html
import re

index_header = {"tag": "span", "id": "Works_by_age"}
index_end = {"tag": "span", "id": "About"}

class IndexParser(HTMLParser):
    def __init__(self, url_root):
        super().__init__()
        self.url_root = url_root

        self.book_url_dict = {}

        self.html = None
        self.soup = None

        self.index_started = False
        self.parse_next_data = 0

        self.current_category = ""
        self.current_book_href = ""
        self.current_author = ""
        self.current_author_href = ""
        self.current_date = ""
        self.current_book_title = ""

    def feed(self, data: str) -> None:
        self.html = data
        self.soup = BeautifulSoup(self.html, 'html.parser')
        HTMLParser.feed(self, data)

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == index_header["tag"] and "id" in attr_dict.keys() and attr_dict["id"] == index_header["id"]:
            self.index_started = True
        elif tag == index_end["tag"] and "id" in attr_dict.keys() and attr_dict["id"] == index_end["id"]:
            self.index_started = False
        elif tag == "span" and self.index_started and "class" in attr_dict.keys() and attr_dict["class"] == "mw-headline":
            raw_category = attr_dict["id"]

            if raw_category[0] == "0":
                self.current_category = "0+"
            else:
                self.append_current_book()
                self.current_category = raw_category
        elif tag == "a" and self.index_started and "href" in attr_dict.keys() and "/wiki/" in attr_dict["href"]:
            if "Author:" in attr_dict["href"]:
                self.current_author = attr_dict["href"].split(':')[1].replace('_', ' ')
                self.current_author_href = attr_dict["href"]
                self.parse_next_data = 2
            else:
                if len(self.current_book_href) > 0:
                    self.append_current_book()
                self.current_book_href = attr_dict["href"]
                self.current_book_title = attr_dict["title"]

    def handle_data(self, data: str) -> None:
        if self.parse_next_data > 0:
            match = re.search(r'\(\d{4}\)', data)

            if "All other books by" in data:
                author_parser = AuthorParser(self.url_root, self.current_author, self.current_category)
                author_parser.feed(retrieve_html(self.url_root + self.current_author_href))
                self.append_book_list(self.current_category, self.current_author, author_parser.get_book_list())

            if match is not None:
                self.current_date = match.group(0).replace('(', '').replace(')', '')

            self.parse_next_data -= 1

    def append_book_list(self, category, author, book_list):
        for book in book_list:
            self.book_url_dict[category].append((book['href'], book['title'], author, book['date']))

    def append_current_book(self):
        if self.current_category not in self.book_url_dict:
            self.book_url_dict[self.current_category] = []
        self.book_url_dict[self.current_category].append((self.current_book_href, self.current_book_title, self.current_author, self.current_date))
        self.current_book_href = ""
        self.current_author = ""
        self.current_date = ""
        self.current_book_title = ""


    def retrieve_result(self):
        self.append_current_book()
        return self.book_url_dict
