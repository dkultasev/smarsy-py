import unittest
import sys
import os

from unittest.mock import patch, PropertyMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..', 'smarsy')))
# excluding following line for linter as it complains that
# from import is supposed to be at the top of the file

from smarsy.bs_helper import BSHelper # noqa


class TestBSHelperInstance(unittest.TestCase):
    def setUp(self):
        self.html = 'some html'
        self.source_page = BSHelper(self.html)

    def test_bshelper_instance_created(self):
        self.assertEqual(self.source_page.html, self.html)


class TestGetPageSource(unittest.TestCase):
    @patch('smarsy.bs_helper.BeautifulSoup', new_callable=PropertyMock)
    def test_get_bs_object_called_with_expected_html(self, mocked_soup):
        html = '<tr></tr>'
        source_page = BSHelper(html)
        source_page.get_bs_object
        mocked_soup.assert_called_with(html, 'html.parser')

    @patch('smarsy.bs_helper.BeautifulSoup', side_effect=TypeError)
    def test_get_bs_object_return_false_with_unexpected_html(
             self, mocked_soup):
        source_page = BSHelper(12345)
        self.assertFalse(source_page.get_bs_object)


class TestBsSafeSelect(unittest.TestCase):
    @patch('smarsy.bs_helper.BeautifulSoup')
    def setUp(self, mocked_soup):
        self.source_page = BSHelper('some html')
        self.mocked_soup = mocked_soup
        self.mocked_soup.select_one.return_value = 'some text'
        self.selector = 'some_tag'

    def test_bs_safe_select_return_expected_text_with_single_selector(self):
        actual = self.source_page.bs_safe_select(self.mocked_soup,
                                                 self.selector)
        self.assertEqual(actual, 'some text')

    def test_bs_safe_select_return_expected_text_with_many_selectors(self):
        selector1, selector2, selector3 = 'some_tag1', 'some_tag2', 'some_tag3'
        actual = self.source_page.bs_safe_select(self.mocked_soup, selector1,
                                                 selector2, selector3)
        self.assertEqual(actual, 'some text')

    def test_bs_safe_select_return_false_when_selectedElems_is_empty(
             self):
        self.mocked_soup.select_one.return_value = ''
        self.assertFalse(self.source_page.bs_safe_select(self.mocked_soup,
                                                         self.selector))
