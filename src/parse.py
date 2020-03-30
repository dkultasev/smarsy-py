import requests
from bs4 import BeautifulSoup


def get_page_content(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    else:
        raise requests.HTTPError("Error code - {}".format(r.status_code))


def validate_title(html):
    if BeautifulSoup(html, 'html.parser').title.text == \
                     'Smarsy - Смарсі - Україна':
        return True
    else:
        raise Exception
