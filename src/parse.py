import requests


def get_login_page(url):
    r = requests.get(url)
    if r.status_code == 200:
        return 'sdfsfsf'
    else:
        pass


def get_credentials(parameter_list):
    pass
