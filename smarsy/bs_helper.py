from bs4 import BeautifulSoup


class BSHelper(object):
    """
     The help class for BeautifulSoup library
     """
    def __init__(self, html):
        self.html = html

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
