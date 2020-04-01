import requests
from bs4 import BeautifulSoup
import json
import os


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
        basedir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                               '..', 'cfg'))
        with open(os.path.join(basedir, filename)) as f:
            return json.load(f)
    except IOError:
        raise IOError('{} does not exist.'.format(filename))
    except ValueError:
        raise ValueError('{} is not valid JSON.'.format(filename))


def get_user_credentials():
    login = open_json_file('login.json')
    em = 'Credentials are in the wrong format ({} is missing)'
    for key in ('language', 'username', 'password'):
        if key in login.keys():
            continue
        raise Exception(em.format(key))
    return login
