import requests
import sys
from bs4 import BeautifulSoup


def get_page_content(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.text
    except requests.HTTPError as err:
        return err


def validate_title(html):
    if BeautifulSoup(html, 'html.parser').title.text == \
                     'Smarsy - Смарсі - Україна':
        return True
    else:
        raise Exception



# def validate_login_page_source(html):
#     try:
#         if html.startswith('<html>') and html.endswith('</html>') \
#            and BeautifulSoup(html, 'html.parser').title.text ==  \
#            'Smarsy - Смарсі - Україна':
#             return BeautifulSoup(html, 'html.parser').title.text
#     except:
#         raise ValueError('Invalid title in the page source')
#         print('Invalid title in the page source')
#         sys.exit()



def get_credentials(parameter_list):
    pass
