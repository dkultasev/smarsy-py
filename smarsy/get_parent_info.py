from bs4 import BeautifulSoup
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..')))

from smarsy.parse import convert_to_date_from_russian_written # noqa


class ParseParentData(object):
    """
    The class receives HTML page(Response.text) and store the data of parent(s)
    as a list of dictionaries or an empty list
    """
    def __init__(self, html):
        self.html = html
        self.parentsdata = None

    @property
    def get_bs_object(self):
        """
        Utility funtcion:
            - Accepts html and checks its validity using BeautifulSoup library,
              return BS object or False
        """
        try:
            soup = BeautifulSoup(self.html, 'html.parser')
        except TypeError:
            return False
        return soup

    def get_parents_table(self, soup):
        """
        Utility funtcion:
            - Accepts soup and checks if parents table excists.
              If excists return parents table chidren list or False
        """
        parents_tab = soup.select_one('table')
        if parents_tab is not None and len(parents_tab) > 0:
            parents_table_chidren_list = self.get_parents_table_chidren(
                    parents_tab)
            if parents_table_chidren_list is not None:
                return parents_table_chidren_list
        return False

    def get_parents_table_chidren(self, parents_table_html):
        """
        Utility funtcion:
            - Accepts parents table html and return children list_iterator
        """
        parents_tab_chidren = parents_table_html.childGenerator()
        return parents_tab_chidren

    def get_parents_data(self, parent_data_list):
        """
        Utility funtcion:
            - Accepts parents data table list_iterator and
            return parent data
        """
        for parent in parent_data_list:
            parent_img = self.get_parents_img(parent)
            parent_fullname = self.get_parents_fullname(parent)
            parent_fullname = self.get_parents_bdate(parent)

    def get_parents_img(self, parent_data_html):
        """
        - Accepts parents data html and
            return link to parents image
        """
        img_html = self.bs_safe_select(parent_data_html,
                                       '[valign=top]', 'img[src]')
        if img_html:
            img_url = self.bs_safe_get(img_html, 'src')
            if img_url:
                return img_url
            else:
                return 'No image'

    def get_parents_fullname(self, parent_data_html):
        """
        - Accepts parents data html and
            return parent_name, parent_surname,
            parent_middlename, parent_type
        """
        parents_fullname_html = self.bs_safe_select(parent_data_html,
                                                    '.username')
        if parents_fullname_html:
            parents_fullname = parents_fullname_html.get_text()
            if parents_fullname:
                parents_fullname_list = parents_fullname.split(' ')
                return (parents_fullname_list[0], parents_fullname_list[1],
                        parents_fullname_list[2],
                        parents_fullname_list[3][1:-1])
            else:
                return 'No parents fullname'

    def get_parents_bdate(self, parent_data_html):
        """
        - Accepts parents data html and
            returns parent_birth_date
        """
        parents_bdate_html = self.bs_safe_select(parent_data_html,
                                                 '.userdata')
        if parents_bdate_html:
            parents_bdate = parents_bdate_html.get_text()
            if parents_bdate:
                parents_bdate_in_right_format = str(
                    convert_to_date_from_russian_written(parents_bdate))
            else:
                return 'No parents birthday'

    def bs_safe_select(self, html, *args):
        """
        Utility function used to get a content string from a
        HTML and tuple of selectors. Returns False
        if no object is found for the given selector
        """
        for arg in args:
            selectedElems = html.select_one(arg)
        if selectedElems is not None:
            return selectedElems
        return False

    def bs_safe_get(self, html, attribute):
        """
        Utility function used to get a content string from a
        HTML and attribute. Returns False
        if no object is found for the given selector
        """
        element = html.get(attribute)
        if element is not None:
            return element
        return False

    def parse_logic(self):
        """
        Main class logic funtcion:
            - Cheks soup is if True - pass, Else
            parentsdata = 'Нет данных о родителях'
            - Cheks for parent table if True - pass,
              Else parentsdata = 'Родительская таблица пуста'
            - Cheks for data in parent table children if True - pass,
              Else parentsdata = empty list
            - For each parent parse 'parent_img', 'parent_name',
            'parent_surname', 'parent_middlename', 'parent_type',
            'parent_birth_date'
            - Creates parents data
        """
        soup = self.get_bs_object
        if soup:
            parents_tab = self.get_parents_table(soup)
            if parents_tab:
                parent_data = self.get_parents_data(parents_tab)
            else:
                self.parentsdata = 'Родительская таблица пуста'
        else:
            self.parentsdata = 'Нет данных о родителях'
