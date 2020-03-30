from unittest.mock import patch

import unittest
import requests
import subprocess
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# excluding following line for linter as it complains that
# from import is supposed to be at the top of the file
from src.parse import (get_page_content, validate_title) # noqa


class TestsGetPage(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('requests.get')
    def test_right_url(self, mock_request):
        mock_request.return_value.status_code = 200
        exepted_url = 'https://smarsy.ua/'
        get_page_content(exepted_url)
        mock_request.assert_called_with('')

    @patch('requests.get')
    def test_response_status_code_ok(self, mock_response):
        url = 'https://smarsy.ua/'
        mock_response.return_value.status_code = 200
        expected_text = 'This is login Page'
        mock_response(url).text = expected_text
        self.assertEqual(get_page_content(url), expected_text)

    @patch('requests.get')
    def test_response_status_code_404(self, mock_response):
        url = 'https://smarsy.ua/'
        mock_response.return_value.status_code = 404
        self.assertRaises(requests.HTTPError, get_page_content, url)

    def test_page_title_validate(self):
        html = '<html><title>Smarsy - Смарсі - Україна</title></html>'
        actual = validate_title(html)
        self.assertTrue(actual)


if __name__ == '__main__':
    if '--unittest' in sys.argv:
        subprocess.call([sys.executable, '-m', 'unittest', 'discover']) 
