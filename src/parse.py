import requests
from bs4 import BeautifulSoup
import json
import os


def perform_get_request(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    else:
        raise requests.HTTPError("Error code - {}".format(r.status_code))


def perform_post_request(session, url, data=None, headers=None):
    """
    Performs post request.

    :param session: Request session
    :param url: URL for Request object
    :param data: (optional) Dictionary, list of tuples, bytes, or
      file-like object to send in the body of the Request
    :param headers: (optional) HTTP headers
    :returns: Response text
    :raises HTTPError: raises on reponse status code <> 200
    """
    r = session.post(url=url, data=data, headers=headers)
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


def validate_object_keys(keys, test_json):
    try:
        assert isinstance(keys, (list, tuple))
        for key in keys:
            if key in test_json.keys():
                continue
            raise Exception('Key is missing')
        return True
    except AssertionError:
        raise AssertionError('Keys must be tuple or list.')


def get_user_credentials():
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..', 'cfg', 'login.json'))
    login = open_json_file(file_path)
    em = 'Credentials are in the wrong format ({} is missing)'
    for key in ('language', 'username', 'password'):
        if key in login.keys():
            continue
        raise Exception(em.format(key))
    return login


def get_headers():
    """
    Headers for HTTP request.

    :returns: Headers for HTTP request
    """
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..', 'cfg', 'headers.json'))
    return open_json_file(file_path)


def login():
    """
    Perform login to Smarsy.

    :returns: true on succesful login
    """
    headers = get_headers()
    a = 0