import requests


def get_page_content(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.text
    except requests.HTTPError as err:
        return err


def get_credentials(parameter_list):
    pass
