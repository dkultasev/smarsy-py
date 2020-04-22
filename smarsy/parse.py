import json
import locale
import os
import datetime
from typing import List, Tuple, Union

import requests
from bs4 import BeautifulSoup

from enums import Urls


def perform_get_request(session, url, params=None, headers=None):
    r = session.get(url=url, params=params, headers=headers)
    if r.status_code == 200:
        return r.text
    else:
        raise requests.HTTPError("Error code - {}".format(r.status_code))


def perform_post_request(session, url, data=None, headers=None, encoding=None):
    """
    Performs post request.

    :param session: `Request` session
    :param url: URL for `Request` object
    :param data: (optional) Dictionary, list of tuples, bytes, or
      file-like object to send in the body of the `Request`
    :param headers: (optional) HTTP headers
    :returns: Response text
    :raises HTTPError: raises on reponse status code <> 200
    """
    r = session.post(url=url, data=data, headers=headers)
    r.encoding = encoding
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


def validate_object_keys(keys: Union[Tuple[str], List[str]], test_json):
    if len(keys):
        for key in keys:
            if key in test_json.keys():
                continue
            raise Exception('Key is missing')
        return True
    else:
        raise Exception('Key is empty')


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


def childs_page_return_right_login(response_page, smarsy_login):
    """
    Receive HTML page from login function and check we've got expected source
    """
    if smarsy_login in response_page:
        return True
    else:
        raise ValueError('Invalid Smarsy Login')


def convert_to_date_from_russian_written(date_in_str, format='%d %B %Y г.'):
    locale.setlocale(locale.LC_TIME, 'ru_RU')
    try:
        date_with_time = datetime.datetime.strptime(date_in_str, format)
        return date_with_time.date()
    except:
        raise ValueError('Wrong date format')


def login():
    """
    Perform login to Smarsy.

    :returns: true on succesful login
    """
    session = requests.Session()
    response = perform_post_request(session,
                                    Urls.LOGIN.value,
                                    get_user_credentials(),
                                    get_headers())
    return response


def bs_safeget(soup, *args):
    """
        Utility function used to get a content string from a
        Beautiful Soup object and tuple of selectors. Returns False
        if no object is found for the given selector
        """
    if len(args) == 1:
        selectedElems = soup.select(args[0])
    else:
        for arg in args:
            selectedElems = soup.select(arg)
    if selectedElems is not None and len(selectedElems) > 0:
        return selectedElems[0]
    return False


def get_parents_img(parent_html, *args):
    """
    Function receive: HTML, tags for search and return parents img URL
    """
    return bs_safeget(parent_html, *args)


def get_parents_name(parent_html, *args):
    """
    Function receive: HTML, tags for search and return parents full name
    """
    return bs_safeget(parent_html, *args)


def get_parents_b_date(parent_html, *args):
    """
    Function receive: HTML, tags for search and return parents b_date
    """
    return bs_safeget(parent_html, *args)


def create_parents_dict(parent_html) -> dict:
    """
    Function receive HTML and return parent dictionary with given keys
    """
    parent_dict = {}
    parent_list = []
    parents_keys = ['parent_img', 'parent_name', 'parent_surname',
                    'parent_middlename', 'parent_type',
                    'parent_birth_date']
    parent_img = get_parents_img(parent_html, '[valign=top]', 'img[src]')
    if parent_img:
        parent_list.append(parent_img.attrs['src'])
    parents_fullname = get_parents_name(parent_html, '.username')
    if parents_fullname:
        parents_name = parents_fullname.text.split(' ')
        parent_list.append(parents_name[0])
        parent_list.append(parents_name[1])
        parent_list.append(parents_name[2])
        parent_list.append(parents_name[3][1:-1])
    parent_b_date = get_parents_b_date(parent_html, '.userdata')
    if parent_b_date:
        parent_list.append(
            str(convert_to_date_from_russian_written(parent_b_date.text)))
    for parents_key, parent_value in zip(
            parents_keys, parent_list):
        parent_dict[parents_key] = parent_value
    return parent_dict


def parent_page_content_to_object(html) -> list:
    try:
        soup = BeautifulSoup(html, 'html.parser')
        parent_tab = bs_safeget(soup, 'table')
        parents = []
        if parent_tab:
            for parent in parent_tab.children:
                parents.append(create_parents_dict(parent))
        else:
            pass
        return parents
    except:
        raise TypeError('Wrong file format')
