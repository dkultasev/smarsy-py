from unittest.mock import patch

import unittest
import requests
import subprocess
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# excluding following line for linter as it complains that
# from import is supposed to be at the top of the file
from src.parse import (get_page_content, validate_title, read_json)  # noqa


class TestsGetPage(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('requests.get')
    def test_right_url_is_passed_to_reponse_get_is(self, mock_request):
        mock_request.return_value.status_code = 200
        exepted_url = 'https://smarsy.ua/'
        get_page_content(exepted_url)
        mock_request.assert_called_with(exepted_url)

    @patch('requests.get')
    def test_response_with_status_200_returns_expected_text(self,
                                                            mock_response):
        url = 'https://smarsy.ua/'
        mock_response.return_value.status_code = 200
        expected_text = 'This is login Page'
        mock_response(url).text = expected_text
        self.assertEqual(get_page_content(url), expected_text)

    @patch('requests.get')
    def test_response_with_status_code_404_raises_exception(self,
                                                            mock_response):
        url = 'https://smarsy.ua/'
        mock_response.return_value.status_code = 404
        self.assertRaises(requests.HTTPError, get_page_content, url)

    def test_login_page_has_expected_title(self):
        html = '<html><title>Smarsy - Смарсі - Україна</title></html>'
        actual = validate_title(html)
        self.assertTrue(actual)


class TestsFileOperations(unittest.TestCase):
    @patch('json.load')
    def test_read_json_filepath_passed_to_json_load(self,
                                                    mock_json_load):
        file_path = 'some path'
        read_json(file_path)
        mock_json_load.assert_called_with(file_path)

    @patch('json.load')
    def test_read_json_data_from_file_is_returned(self,
                                                  mock_json_load):
        file_path = 'some_path'
        expected_json = {'id': 1}
        mock_json_load.return_value = expected_json
        self.assertEqual(read_json(file_path), expected_json)


if __name__ == '__main__':
    if '--unittest' in sys.argv:
        subprocess.call([sys.executable, '-m', 'unittest', 'discover'])
