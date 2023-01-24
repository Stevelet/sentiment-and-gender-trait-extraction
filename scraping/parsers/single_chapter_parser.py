from html.parser import HTMLParser
import re


class SingleChapterParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.store_data = False
        self.tag_stack = []
        self.data = ""

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)

        self.tag_stack.append(tag)

        if tag == "div" and "class" in attr_dict.keys() and "prp-pages-output" in attr_dict["class"]:
            pass
        if tag == "noscript":
            self.store_data = False
        if 'class' in attr_dict.keys() and 'licenseContainer' in attr_dict['class']:
            self.store_data = False

    def handle_endtag(self, tag: str) -> None:
        top = self.tag_stack.pop()

    def handle_data(self, data: str) -> None:
        if 'mw-parser-output' in data or 'wst-block-center' in data:
            self.store_data = True
        if 'dynlayout-exempt-footer' in data:
            self.store_data = False

        if self.store_data is True and self.tag_stack[-1] in ["span", "p", "div"]:
            parsed_data = data.replace('\\n', '\n').replace('\\d', '\'')
            self.data += parsed_data

    def retrieve_text(self):
        return self.data
