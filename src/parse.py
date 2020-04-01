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


def open_json_file(filename):
    try:
        with open(filename) as f:
            return json.load(f)
    except IOError:
        raise IOError('{} does not exist.'.format(filename))
    except ValueError:
        raise ValueError('{} is not valid JSON.'.format(filename))


def get_user_credentials():
    login = open_json_file('../cfg/login.json')
    em = 'Credentials are in the wrong format ({} is missing)'
    if 'language' not in login.keys():
        raise Exception(em.format('language'))
    if 'username' not in login.keys():
        raise Exception(em.format('username'))
    if 'password' not in login.keys():
        raise Exception(em.format('password'))
    return login
