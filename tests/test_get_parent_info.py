import unittest
import sys
import os

from unittest.mock import patch, PropertyMock

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
    @patch('smarsy.get_parent_info.BeautifulSoup', new_callable=PropertyMock)
    def test_get_bs_object_called_with_expected_html(self, mocked_soup):
        html = '<tr></tr>'
        source_page = ParseParentData(html)
        source_page.get_bs_object
        mocked_soup.assert_called_with(html, 'html.parser')

    @patch('smarsy.get_parent_info.BeautifulSoup', side_effect=TypeError)
    def test_get_bs_object_return_false_with_unexpected_html(
            self, mocked_soup):
        source_page = ParseParentData(12345)
        self.assertFalse(source_page.get_bs_object)


class TestGetParentsTab(unittest.TestCase):
    def setUp(self):
        self.source_page = ParseParentData('some html')

    @patch('smarsy.get_parent_info.BeautifulSoup.select_one')
    def test_bs_select_one_called_with_expected_params(
            self, mocked_bs_select_one):
        self.source_page.parse_logic()
        mocked_bs_select_one.assert_called_with('table')

    @patch('smarsy.get_parent_info.BeautifulSoup')
    def test_return_expected_html_if_parents_table(self, mocked_bs):
        mocked_bs.select_one.return_value = 'some table'
        actual = self.source_page.get_parents_table(mocked_bs)
        self.assertEqual(actual, 'some table')

    @patch('smarsy.get_parent_info.BeautifulSoup')
    def test_return_false_html_if_parents_table_is_none(self, mocked_bs):
        mocked_bs.select_one.return_value = None
        actual = self.source_page.get_parents_table(mocked_bs)
        self.assertFalse(actual)


class TestGetParentsTabChildren(unittest.TestCase):
    def setUp(self):
        self.source_page = ParseParentData('some html')

    @patch('smarsy.get_parent_info.BeautifulSoup')
    def test_bs_select_called_with_expected_params(self, mocked_bs):
        self.source_page.get_parents_table_chidren(mocked_bs)
        mocked_bs.childGenerator.assert_called()

    @patch('smarsy.get_parent_info.BeautifulSoup')
    def test_return_expected_html_if_children(self, mocked_bs):
        mocked_bs.childGenerator.return_value = 'some table'
        actual = self.source_page.get_parents_table_chidren(mocked_bs)
        self.assertEqual(actual, 'some table')

    @patch('smarsy.get_parent_info.BeautifulSoup')
    def test_return_false_html_if_children_is_none(self, mocked_bs):
        mocked_bs.childGenerator.return_value = None
        actual = self.source_page.get_parents_table_chidren(mocked_bs)
        self.assertFalse(actual)


class TestParseLogic(unittest.TestCase):
    def setUp(self):
        self.source_page = ParseParentData('some html')

    @patch('smarsy.get_parent_info.ParseParentData.get_bs_object',
           new_callable=PropertyMock)
    def test_get_bs_object_called(self, mocked_bs):
        self.source_page.parse_logic()
        mocked_bs.assert_called_once()

    @patch('smarsy.get_parent_info.ParseParentData.get_bs_object',
           return_value=False)
    def test_parentsdata_is_empty_with_wrong_soup(self, mocked_bs):
        self.source_page.parse_logic()
        self.assertIsNone(self.source_page.parentsdata)

    @patch('smarsy.get_parent_info.ParseParentData.get_parents_table')
    @patch('smarsy.get_parent_info.ParseParentData.get_bs_object',
           new_callable=PropertyMock, return_value='some soup')
    def test_get_parents_table_called_with_expected_params(
            self, mocked_bs, mocked_get_parents_tab):
        soup = 'some soup'
        self.source_page.parse_logic()
        mocked_get_parents_tab.assert_called_with(soup)

    @patch('smarsy.get_parent_info.ParseParentData.get_parents_table')
    @patch('smarsy.get_parent_info.ParseParentData.get_bs_object',
           new_callable=PropertyMock, return_value=False)
    def test_get_parents_table_not_called_if_soup_is_none(
            self, mocked_bs, mocked_get_parents_tab):
        self.source_page.parse_logic()
        mocked_get_parents_tab.assert_not_called()

    @patch('smarsy.get_parent_info.ParseParentData.get_parents_table',
           return_value=False)
    def test_parentsdata_is_none_with_none_parents_table(self, mocked_table):
        self.source_page.parse_logic()
        self.assertIsNone(self.source_page.parentsdata)

    @patch('smarsy.get_parent_info.ParseParentData.get_parents_table_chidren')
    @patch('smarsy.get_parent_info.ParseParentData.get_parents_table',
           return_value="some parents_table")
    def test_children_called_with_expected_params(self, mocked_table,
                                                  mocked_get_chidren):
        """
            Test if get_parents_tab_children called with expected params
        """
        self.source_page.parse_logic()
        mocked_get_chidren.assert_called_with('some parents_table')

    @patch('smarsy.get_parent_info.ParseParentData.get_parents_table_chidren')
    @patch('smarsy.get_parent_info.ParseParentData.get_parents_table',
           return_value=False)
    def test_children_not_called_if_parents_table_is_none(
            self, mocked_table, mocked_get_chidren):
        """
        Test if get_parents_tab_children not called if parents tab is none
        """
        self.source_page.parse_logic()
        mocked_get_chidren.assert_not_called()

    @patch('smarsy.get_parent_info.ParseParentData.get_parents_table_chidren',
           return_value=False)
    def test_parentsdata_is_none_if_parents_table_has_no_children(
            self, mocked_get_chidren):
        """
        Test parentsdata is still None if parents tab has no children tags
        """
        self.source_page.parse_logic()
        self.assertIsNone(self.source_page.parentsdata)

    @patch('smarsy.get_parent_info.ParseParentData.get_parents_data')
    @patch('smarsy.get_parent_info.ParseParentData.get_parents_table_chidren',
           return_value="some parents_table children html")
    def test_parse_parent_data_called_with_expected_params(
            self, mocked_parents_table_chidren_list, mocked_get_parents_data):
        self.source_page.parse_logic()
        mocked_get_parents_data.assert_called_with(
            'some parents_table children html')

    @patch('smarsy.get_parent_info.ParseParentData.get_parents_data')
    @patch('smarsy.get_parent_info.ParseParentData.get_parents_table_chidren',
           return_value=False)
    def test_parse_parent_data_not_called_if_children_table_is_none(
            self, mocked_parents_table_chidren_list, mocked_get_parents_data):
        self.source_page.parse_logic()
        mocked_get_parents_data.assert_not_called()

    @patch('smarsy.get_parent_info.ParseParentData.get_parents_data',
           return_value=False)
    def test_parentsdata_is_none_if_children_table_is_none(
            self, mocked_get_parents_data):
        self.source_page.parse_logic()
        self.assertIsNone(self.source_page.parentsdata)