from bs4 import BeautifulSoup


class BSHelper(object):
    """
     The help class for BeautifulSoup library
     """
    def __init__(self, html):
        self.html = html

    @property
    def bs_object(self):
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
