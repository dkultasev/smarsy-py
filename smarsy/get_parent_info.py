from bs4 import BeautifulSoup


class ParseParentData(object):
    """
    The class receives HTML page(Response.text) and store the data of parent(s)
    as a list of dictionaries or an empty list
    """
    def __init__(self, html):
        self.html = html
        self.parentsdata = None

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
            - Accepts soup and checks if parents table excists,
              return parents table or False
        """
        parents_tab = soup.select('table')

    def parse_logic(self):
        """
        Main class logic funtcion:
            - Cheks soup is if True - pass, Else parentsdata = None
            - Cheks for parent table if True - pass,
              Else parentsdata = empty list
            - Cheks for data in parent table if True - pass,
              Else parentsdata = empty list
            - For each parent parse 'parent_img', 'parent_name',
            'parent_surname', 'parent_middlename', 'parent_type',
            'parent_birth_date'
            - Creates parents data
        """
        soup = self.get_bs_object()
        if soup:
            parents_tab = self.get_parents_table(soup)
