import os
import sys
import unittest
from unittest.mock import patch
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.parse import get_login_page


class Tests_Login(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('requests.get')
    def test_right_url(self, mock_request):
        exepted_url = 'https://smarsy.ua/'
        get_login_page(exepted_url)
        mock_request.assert_called_with(exepted_url)

    @patch('requests.get')
    def test_response_status_code_ok(self, mock_response):
        url = 'https://smarsy.ua/'
        mock_response.return_value.status_code = 200
        get_login_page(url)
        expected_text = 'This is login Page'
        mock_response(url).text = expected_text
        self.assertEqual(get_login_page(url), expected_text)

    @patch('requests.get')
    def test_response_status_code_404(self, mock_response):
        url = 'https://smarsy.ua/'
        mock_response.return_value.status_code = 404
        self.assertRaises(requests.HTTPError, get_login_page(url))

    # def test_read_credentials_from_file(self):

    # def test_get_user_credentials(self):
    #     expected_creds = {'login': 'user', 'password': ''}
    #     actual_creds = get_credentials()
    #     self.assertEqual(expected_creds, actual_creds)


if __name__ == "__main__":
    unittest.main(verbosity=1)
