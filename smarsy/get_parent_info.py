from bs4 import BeautifulSoup


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
            return parent data or False
        """
        pass

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
