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
