import requests


def get_login_page(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    elif r.status_code == 400:
        r.text == 'Page not Found'
        return r.text


def get_credentials(parameter_list):
    pass
