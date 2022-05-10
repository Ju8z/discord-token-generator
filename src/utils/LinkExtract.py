from bs4 import BeautifulSoup


class LinkExtractor:
    def __init__(self, html_string):
        soup = BeautifulSoup(html_string, "html.parser")
        for link in soup.findAll('a'):
            if "Verify Email" in link.text:
                print(link.get('href'))
                self.out_link = link.get('href')
