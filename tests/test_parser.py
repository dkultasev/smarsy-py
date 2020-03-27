import os
import sys
import unittest
from unittest.mock import patch
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.parse import get_page_content, validate_login_page_source


class TestsGetPage(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('requests.get')
    def test_right_url(self, mock_request):
        exepted_url = 'https://smarsy.ua/'
        get_page_content(exepted_url)
        mock_request.assert_called_with(exepted_url)

    @patch('requests.get')
    def test_response_status_code_ok(self, mock_response):
        url = 'https://smarsy.ua/'
        mock_response.return_value.status_code = 200
        get_page_content(url)
        expected_text = 'This is login Page'
        mock_response(url).text = expected_text
        self.assertEqual(get_page_content(url), expected_text)

    @patch('requests.get')
    def test_response_status_code_404(self, mock_response):
        url = 'https://smarsy.ua/'
        mock_response.return_value.status_code = 404
        self.assertRaises(requests.HTTPError, get_page_content(url))

    # def test_login_page(self, mock_response):
    #     # url действительно тот, что нам нужен
    #     url = 'https://smarsy.ua/'
    #     mock_response.return_value

    def test_validate_login_page_source_returns_true_with_valid_title(self):
        html = '<html><title>Smars - Смарсі - Україна</title></html>'
        actual = validate_login_page_source(html)
        expected_title = 'Smarsy - Смарсі - Україна'
        if actual:
            self.assertEqual(actual, expected_title)
        else:
            self.assertRaises(ValueError, actual)
            print('Invalid title in the page source')


    # def test_read_credentials_from_file(self):

    # def test_get_user_credentials(self):
    #     expected_creds = {'login': 'user', 'password': ''}
    #     actual_creds = get_credentials()
    #     self.assertEqual(expected_creds, actual_creds)


if __name__ == "__main__":
    unittest.main(verbosity=1)
