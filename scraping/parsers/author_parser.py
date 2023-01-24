from html.parser import HTMLParser
import re

index_header = {"tag": 'span', 'id': 'Children.27s_books'}
index_end = {'tag': 'div', "class": 'licenseContainer licenseBanner dynlayout-exempt'}

class AuthorParser(HTMLParser):
    def __init__(self, url_root, category, author):
        super().__init__()
        self.category = category
        self.author = author
        self.index_started = False
        self.parse_next_data = 0

        self.current_book_href = ""
        self.current_date = ""
        self.current_book_title = ""

        self.books = []


    def feed(self, data: str) -> None:
        HTMLParser.feed(self, data)

    def get_book_list(self):
        return self.books


    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == index_header["tag"] and "id" in attr_dict.keys() and attr_dict["id"] == index_header["id"]:
            self.index_started = True
        if tag == index_end["tag"] and 'class' in attr_dict.keys() and attr_dict['class'] == index_end['class']:
            self.index_started = False
        if tag == 'li' and self.index_started:
            self.parse_next_data = 1
        if tag == 'a' and self.parse_next_data > 0:
            self.current_book_href = attr_dict['href']
            self.current_book_title = attr_dict['title']

    def handle_data(self, data: str) -> None:
        if self.parse_next_data > 0 and not self.current_book_title == data:
            self.current_date = re.sub('[^0-9]','', data)
            self.parse_next_data -= 1
            self.append_current_book()

    def append_current_book(self):
        self.books.append({'href': self.current_book_href, 'title': self.current_book_title, 'date': self.current_date})