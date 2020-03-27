import os
import sys
import unittest
from unittest.mock import patch

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
    def test_response_status_code(self, mock_response):
        url = 'https://smarsy.ua/'
        mock_response.return_value.status_code = 200
        get_login_page(url)
        response_text = mock_response.text
        self.assertEqual(get_login_page(url), response_text)
    # def test_read_credentials_from_file(self):

    # def test_get_user_credentials(self):
    #     expected_creds = {'login': 'user', 'password': ''}
    #     actual_creds = get_credentials()
    #     self.assertEqual(expected_creds, actual_creds)


if __name__ == "__main__":
    unittest.main(verbosity=1)
