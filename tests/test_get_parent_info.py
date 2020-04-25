import unittest
import sys
import os

from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..',
                                             'smarsy')))
# excluding following line for linter as it complains that
# from import is supposed to be at the top of the file

from smarsy.get_parent_info import ParseParentData # noqa


class TestParseParentData(unittest.TestCase):
    def setUp(self):
        self.html = 'some html'
        self.source_page = ParseParentData(self.html)

    def test_parse_parent_instance_created_with_right_html(self):
        self.assertEqual(self.source_page.html, self.html)

    def test_parents_data_of_a_new_instance_should_be_None(self):
        self.assertIsNone(self.source_page.parentsdata)


class TestGetPageSource(unittest.TestCase):
    @patch('smarsy.get_parent_info.BeautifulSoup')
    def test_get_bs_object_called_with_expected_html(self, mocked_soup):
        html = '<tr></tr>'
        source_page = ParseParentData(html)
        source_page.get_bs_object()
        mocked_soup.assert_called_with(html, 'html.parser')

    @patch('smarsy.get_parent_info.BeautifulSoup', side_effect=TypeError)
    def test_get_bs_object_return_false_with_unexpected_html(
            self, mocked_soup):
        source_page = ParseParentData(12345)
        self.assertFalse(source_page.get_bs_object())


class TestParseLogic(unittest.TestCase):
    @patch('smarsy.get_parent_info.ParseParentData.get_bs_object')
    def test_get_bs_object_called(self, mocked_bs):
        source_page = ParseParentData('some html')
        source_page.parse_logic()
        mocked_bs.assert_called_once()

    @patch('smarsy.get_parent_info.ParseParentData.get_bs_object',
           return_value=False)
    def test_parentsdata_is_empty_with_wrong_soup(self, mocked_bs):
        source_page = ParseParentData('some html')
        source_page.parse_logic()
        self.assertEqual(source_page.parentsdata, [''])
