from unittest.mock import patch, mock_open, MagicMock

import unittest
import requests
import subprocess
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# excluding following line for linter as it complains that
# from import is supposed to be at the top of the file
from src.parse import (get_page_content, validate_title,
                       get_user_credentials,
                       open_json_file)  # noqa


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
    @patch('src.parse.open_json_file')
    def test_user_credentials_object_is_the_same_like_in_file(self,
                                                              mock_json_load):
        expected = {
            'language': 'UA',
            'username': 'user',
            'password': 'pass'
        }
        mock_json_load.return_value = expected
        actual = get_user_credentials()
        self.assertEqual(actual, expected)

    @patch('src.parse.open_json_file')
    def test_user_credentials_fails_if_there_is_no_user(self,
                                                        mock_json_load):
        creds = {
            'language': 'UA',
            'notuser': 'user',
            'password': 'pass'
        }
        mock_json_load.return_value = creds
        with self.assertRaises(Exception) as ue:
            get_user_credentials()
        self.assertEqual(
            'Credentials are in the wrong format (username is missing)',
            str(ue.exception))

    @patch('src.parse.open_json_file')
    def test_user_credentials_fails_if_there_is_no_language(self,
                                                            mock_json_load):
        creds = {
            'nolanguage': 'UA',
            'username': 'user',
            'password': 'pass'
        }
        mock_json_load.return_value = creds
        with self.assertRaises(Exception) as ue:
            get_user_credentials()
        self.assertEqual(
            'Credentials are in the wrong format (language is missing)',
            str(ue.exception))

    @patch('src.parse.open_json_file')
    def test_user_credentials_fails_if_there_is_no_password(self,
                                                            mock_json_load):
        creds = {
            'language': 'UA',
            'username': 'user',
            'nopassword': 'pass'
        }
        mock_json_load.return_value = creds
        with self.assertRaises(Exception) as ue:
            get_user_credentials()
        self.assertEqual(
            'Credentials are in the wrong format (password is missing)',
            str(ue.exception))

    @patch('builtins.open')
    @patch('json.load')
    def test_json_load_gets_content_from_provided_file(self,
                                                       stream_mock, 
                                                       mock_json_load):
        expected = 'some_path_to_file'
        stream_mock = MagicMock()
        stream_mock.__enter__.Name = MagicMock(get=MagicMock(Name=expected))
        open_json_file(expected)
        mock_json_load.assert_called_with(expected)

    def test_open_json_file_returns_object_from_provided_file(self):
        read_data = mock_open(read_data=json.dumps({'a': 1, 'b': 2, 'c': 3}))
        with patch('builtins.open', read_data):
            result = open_json_file('filename')
        self.assertEqual({'a': 1, 'b': 2, 'c': 3}, result)

    def test_open_json_file_raise_expected_exception_with_non_existing_path(self):
        # test file does not exist
        with self.assertRaises(IOError) as context:
            open_json_file('null')
        self.assertEqual(
            'null does not exist.', str(context.exception))

    def test_open_json_file_raise_expected_exception_when_invalid_json_in_file(self):
        # test file does not exist
        read_data = mock_open(read_data='')
        with patch("builtins.open", read_data):
            with self.assertRaises(ValueError) as context:
                open_json_file('filename')
            self.assertEqual(
                'filename is not valid JSON.', str(context.exception))


if __name__ == '__main__':
    if '--unittest' in sys.argv:
        subprocess.call([sys.executable, '-m', 'unittest', 'discover'])
