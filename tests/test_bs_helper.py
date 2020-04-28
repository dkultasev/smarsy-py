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
    def test_bshelper_instance_created(self):
        html = 'some html'
        source_page = BSHelper(html)
        self.assertEqual(source_page.html, html)


class Test_bs_object(unittest.TestCase):
    @patch('smarsy.bs_helper.BeautifulSoup', new_callable=PropertyMock)
    def test_bs_object_called_with_expected_html(self, mocked_soup):
        html = '<tr></tr>'
        source_page = BSHelper(html).bs_object
        mocked_soup.assert_called_with(html, 'html.parser')

    @patch('smarsy.bs_helper.BeautifulSoup', side_effect=TypeError)
    def test_bs_object_return_false_with_unexpected_html(
             self, mocked_soup):
        source_page = BSHelper(12345)
        self.assertFalse(source_page.bs_object)


class Test_bs_safe_select(unittest.TestCase):
    @patch('smarsy.bs_helper.BeautifulSoup')
    def setUp(self, mocked_soup):
        self.source_page = BSHelper('some html')
        self.mocked_soup = mocked_soup
        self.mocked_soup.select_one.return_value = 'some text'
        self.selector = 'some_tag'
        self.selectors = 'some_tag1', 'some_tag2', 'some_tag3'
        self.select_one_values = ('some text1', 'some text2', 'some text3')
        self.expected = 'some text'

    def test_bs_safe_select_return_expected_text_with_single_selector(self):
        actual = self.source_page.bs_safe_select(self.mocked_soup,
                                                 self.selector)
        self.assertEqual(actual, self.expected)

    def test_bs_safe_select_return_expected_text_with_many_selectors(self):
        select_one = None
        for select_one_value in self.select_one_values:
            select_one = select_one_value
        self.mocked_soup.select_one.return_value = select_one
        actual = self.source_page.bs_safe_select(self.mocked_soup,
                                                 self.selectors)
        self.assertEqual(actual, select_one)

    def test_bs_safe_select_return_false_when_no_object_is_found(
             self):
        self.mocked_soup.select_one.return_value = ''
        self.assertFalse(self.source_page.bs_safe_select(self.mocked_soup,
                                                         self.selector))


class Test_bs_safe_get(unittest.TestCase):
    @patch('smarsy.bs_helper.BeautifulSoup')
    def setUp(self, mocked_soup):
        self.source_page = BSHelper('some html')
        self.mocked_soup = mocked_soup

    def test_bs_get_called_with_expected_html_and_attribute(self):
        expected_attribute = 'some attribute'
        self.source_page.bs_safe_get(self.mocked_soup, expected_attribute)
        self.mocked_soup.get.assert_called_with(expected_attribute)

    def test_bs_safe_get_return_false_when_element_is_empty(
             self):
        self.mocked_soup.get.return_value = ''
        self.assertFalse(self.source_page.bs_safe_get(self.mocked_soup,
                                                      'some attribute'))

    def test_bs_safe_get_return_expected_text(self):
        self.mocked_soup.get.return_value = 'some text'
        expected_text = 'some text'
        actual = self.source_page.bs_safe_get(self.mocked_soup,
                                              'some attribute')
        self.assertEqual(actual, expected_text)
