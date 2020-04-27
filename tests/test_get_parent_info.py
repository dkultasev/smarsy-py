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
    def test_return_false_html_if_parents_table_is_none(self, mocked_bs):
        mocked_bs.select_one.return_value = None
        actual = self.source_page.get_parents_table(mocked_bs)
        self.assertFalse(actual)

    @patch('smarsy.get_parent_info.ParseParentData.get_parents_table_chidren')
    @patch('smarsy.get_parent_info.BeautifulSoup.select_one',
           return_value="some parents_table")
    def test_children_called_with_expected_params(self, mocked_table,
                                                  mocked_get_chidren):
        """
            Test if get_parents_tab_children called with expected params
        """
        self.source_page.parse_logic()
        mocked_get_chidren.assert_called_with('some parents_table')

    @patch('smarsy.get_parent_info.ParseParentData.get_parents_table_chidren')
    @patch('smarsy.get_parent_info.BeautifulSoup.select_one',
           return_value='')
    def test_children_not_called_if_parents_table_is_empty(
            self, mocked_table, mocked_get_chidren):
        """
        Test if get_parents_tab_children not called if parents tab is empty
        """
        self.source_page.parse_logic()
        mocked_get_chidren.assert_not_called()

    @patch('smarsy.get_parent_info.ParseParentData.get_parents_table_chidren')
    @patch('smarsy.get_parent_info.BeautifulSoup.select_one',
           return_value="some parents_table")
    @patch('smarsy.get_parent_info.BeautifulSoup')
    def test_return_expected_html_if_parents_table(
            self, mocked_bs, mocked_parents_table,
            mocked_parents_table_chidren):
        mocked_parents_table_chidren.return_value = 'some table'
        actual = self.source_page.get_parents_table(mocked_bs)
        self.assertEqual(actual, 'some table')


class TestGetParentsTabChildren(unittest.TestCase):
    @patch('smarsy.get_parent_info.BeautifulSoup')
    def setUp(self, mocked_bs):
        self.source_page = ParseParentData('some html')
        self.mocked_bs = mocked_bs

    def test_bs_childgenerator_called_with_expected_params(self):
        self.source_page.get_parents_table_chidren(self.mocked_bs)
        self.mocked_bs.childGenerator.assert_called()

    def test_return_expected_html_if_children(self):
        self.mocked_bs.childGenerator.return_value = 'some table'
        actual = self.source_page.get_parents_table_chidren(self.mocked_bs)
        self.assertEqual(actual, 'some table')

    def test_return_false_html_if_children_is_none(self):
        self.mocked_bs.childGenerator.return_value = None
        actual = self.source_page.get_parents_table_chidren(self.mocked_bs)
        self.assertIsNone(actual)


class GetParentsData(unittest.TestCase):
    def setUp(self):
        self.source_page = ParseParentData('some html')

    @patch('smarsy.get_parent_info.ParseParentData.get_parents_img')
    def test_get_parents_img_called_with_expected_params(self, mocked_get_img):
        parent_data_list = ['parent_data_list']
        self.source_page.get_parents_data(parent_data_list)
        mocked_get_img.assert_called_with('parent_data_list')


class GetParentsImg(unittest.TestCase):
    def setUp(self):
        self.source_page = ParseParentData('some html')

    @patch('smarsy.get_parent_info.ParseParentData.bs_safe_select')
    def test_safe_select_called_with_expected_tag(self, mocked_safe_select):
        tag1, tag2 = '[valign=top]', 'img[src]'
        self.source_page.get_parents_img('parent_data_html')
        mocked_safe_select.assert_called_with('parent_data_html', tag1, tag2)

    @patch('smarsy.get_parent_info.ParseParentData.bs_safe_get')
    @patch('smarsy.get_parent_info.ParseParentData.bs_safe_select')
    def test_safe_get_called_with_expected_attribute(
            self, mocked_safe_select, mocked_safe_get):
        mocked_safe_select.return_value = 'some_img_html'
        attribute = 'src'
        self.source_page.get_parents_img('parent_data_html')
        mocked_safe_get.assert_called_with('some_img_html', attribute)

    @patch('smarsy.get_parent_info.ParseParentData.bs_safe_get')
    @patch('smarsy.get_parent_info.ParseParentData.bs_safe_select')
    def test_safe_get_not_called_if_bs_safe_select_return_false(
            self, mocked_safe_select, mocked_safe_get):
        mocked_safe_select.return_value = False
        self.source_page.get_parents_img('parent_data_html')
        mocked_safe_get.assert_not_called()


class TestBsSafeSelect(unittest.TestCase):
    @patch('smarsy.get_parent_info.BeautifulSoup')
    def setUp(self, mocked_soup):
        self.source_page = ParseParentData('some html')
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


class TestBsSafeget(unittest.TestCase):
    @patch('smarsy.get_parent_info.BeautifulSoup')
    def setUp(self, mocked_soup):
        self.source_page = ParseParentData('some html')
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
        actual = self.source_page.bs_safe_get(self.mocked_soup,
                                              'some attribute')
        self.assertEqual(actual, 'some text')


class TestParseLogic(unittest.TestCase):
    def setUp(self):
        self.source_page = ParseParentData('some html')

    @patch('smarsy.get_parent_info.ParseParentData.get_bs_object',
           new_callable=PropertyMock)
    def test_get_bs_object_called(self, mocked_bs):
        self.source_page.parse_logic()
        mocked_bs.assert_called_once()

    @patch('smarsy.get_parent_info.ParseParentData.get_bs_object',
           new_callable=PropertyMock, return_value=False)
    def test_parentsdata_is_expected_none_with_wrong_soup(self, mocked_bs):
        self.source_page.parse_logic()
        expected = 'Нет данных о родителях'
        self.assertEqual(self.source_page.parentsdata, expected)

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
    def test_parentsdata_is_expected_with_none_parents_table(
            self, mocked_table):
        expected = 'Родительская таблица пуста'
        self.source_page.parse_logic()
        self.assertTrue(self.source_page.parentsdata, expected)

    @patch('smarsy.get_parent_info.ParseParentData.get_parents_data')
    @patch('smarsy.get_parent_info.ParseParentData.get_parents_table',
           return_value=None)
    def test_parse_parent_data_not_called_if_parents_table_is_none(
            self, mocked_table, mocked_get_parents_data):
        self.source_page.parse_logic()
        mocked_get_parents_data.assert_not_called()

    @patch('smarsy.get_parent_info.ParseParentData.get_parents_data')
    @patch('smarsy.get_parent_info.ParseParentData.get_parents_table',
           return_value="some parents_table children html")
    def test_parse_parent_data_called_with_expected_params(
            self, mocked_table, mocked_get_parents_data):
        self.source_page.parse_logic()
        mocked_get_parents_data.assert_called_with(
            'some parents_table children html')
