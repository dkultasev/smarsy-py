import requests
from bs4 import BeautifulSoup
import json


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


def read_json(file_path):
    data = json.load(file_path)
    return data


def get_login():
    login = read_json('../cfg/login.json')
    return login
