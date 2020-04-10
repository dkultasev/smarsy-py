from unittest.mock import patch, mock_open, MagicMock, Mock

import unittest
import requests
import subprocess
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..',
                                             'smarsy')))
# excluding following line for linter as it complains that
# from import is supposed to be at the top of the file
from smarsy.parse import (perform_get_request, validate_title,
                       get_user_credentials,
                       open_json_file,
                       perform_post_request,
                       validate_object_keys,
                       get_headers,
                       login,
                       Urls)  # noqa


class MockResponse:
    def __init__(self, status_code=200):
        self.status_code = Mock(status_code=status_code)


@patch('requests.Session')
class TestsGetPage(unittest.TestCase):

    def test_perform_get_request_uses_provided_url_for_request_with_class(
            self, mock_response):
        mock_response.get.return_value = MockResponse().status_code
        exepted_url = 'https://smarsy.ua/'
        perform_get_request(mock_response, exepted_url)
        mock_response.get.assert_called_with(url=exepted_url,
                                             params=None, headers=None)

    def test_perform_get_request_uses_provided_url_for_request(
            self, mock_response):
        mock_response.get.return_value = MockResponse().status_code
        exepted_url = 'https://smarsy.ua/'
        perform_get_request(mock_response, exepted_url)
        mock_response.get.assert_called_with(url=exepted_url,
                                             params=None, headers=None)

    def test_perform_get_request_returns_expected_text_on_valid_request(
            self, mock_response):
        url = 'https://smarsy.ua/'
        mock_response.get.return_value = MockResponse().status_code
        expected_text = 'This is login Page'
        mock_response.get(url).text = expected_text
        self.assertEqual(perform_get_request(mock_response, url),
                         expected_text)

    def test_perform_get_request_resp_with_status_code_404_raises_exception(
            self, mock_response):
        url = 'https://smarsy.ua/'
        mock_response.get.return_value = MockResponse(404).status_code
        self.assertRaises(requests.HTTPError, perform_get_request,
                          mock_response, url)

    def test_perform_get_request_uses_provided_data_for_get_request(
            self, mock_response):
        expected_params = 'data'
        expected_url = 'url'
        mock_response.get.return_value = Mock(status_code=200,
                                              param=expected_params,
                                              text=expected_url)
        perform_get_request(mock_response, expected_url,
                            params=expected_params)
        mock_response.get.assert_called_with(url=expected_url,
                                             params=expected_params,
                                             headers=None)

    def test_perform_get_request_uses_provided_headers_for_get_request(
            self, mock_response):
        expected_headers = {"a": 1}
        expected_url = 'url'
        mock_response.get.return_value = Mock(status_code=200,
                                              params=None,
                                              text=expected_url,
                                              headers=expected_headers)
        perform_get_request(mock_response, expected_url,
                            headers=expected_headers)
        mock_response.get.assert_called_with(url=expected_url, params=None,
                                             headers=expected_headers)


@patch('requests.Session')
class TestsPostRequest(unittest.TestCase):

    def test_perform_post_request_uses_provided_url_for_request(
            self, mock_response):
        mock_response.post.return_value = MockResponse().status_code
        exepted_url = 'https://smarsy.ua/'
        perform_post_request(mock_response, exepted_url)
        mock_response.post.assert_called_with(
            url=exepted_url, data=None, headers=None)

    def test_perform_post_request_returns_expected_text_on_valid_request(
            self, mock_response):
        expected_text = 'some_text'
        mock_response.post.return_value = Mock(text=expected_text,
                                               status_code=200)
        self.assertEqual(perform_post_request(mock_response, 'url'),
                         expected_text)

    def test_perform_post_request_uses_provided_data_for_post_request(
            self, mock_response):
        expected_data = 'data'
        expected_url = 'url'
        mock_response.post.return_value = Mock(status_code=200,
                                               data=expected_data,
                                               text=expected_url)
        perform_post_request(mock_response, expected_url, data=expected_data)
        mock_response.post.assert_called_with(url=expected_url,
                                              data=expected_data,
                                              headers=None)

    def test_perform_post_request_uses_provided_headers_for_post_request(
            self, mock_response):
        expected_headers = {"a": 1}
        expected_url = 'url'
        mock_response.post.return_value = Mock(status_code=200, data=None,
                                               text=expected_url,
                                               headers=expected_headers)
        perform_post_request(mock_response, expected_url,
                             headers=expected_headers)
        mock_response.post.assert_called_with(url=expected_url, data=None,
                                              headers=expected_headers)

    def test_perform_post_request_resp_with_status_code_404_raises_exception(
            self, mock_response):
        expected_text = 'some_text'
        mock_response.post.return_value = Mock(text=expected_text,
                                               status_code=404)
        self.assertRaises(requests.HTTPError, perform_post_request,
                          mock_response, 'url')


class TestsFileOperations(unittest.TestCase):
    @patch('smarsy.parse.open_json_file')
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

    @patch('smarsy.parse.open_json_file')
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

    @patch('smarsy.parse.open_json_file')
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

    @patch('smarsy.parse.open_json_file')
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

    def test_open_json_file_raise_exception_with_non_existing_path(self):
        # test file does not exist
        with self.assertRaises(IOError) as context:
            open_json_file('null')
        self.assertEqual(
            'null does not exist.', str(context.exception))

    def test_open_json_file_raise_exception_when_invalid_json_in_file(self):
        # test file does not exist
        read_data = mock_open(read_data='')
        with patch("builtins.open", read_data):
            with self.assertRaises(ValueError) as context:
                open_json_file('filename')
            self.assertEqual(
                'filename is not valid JSON.', str(context.exception))

    def test_validate_object_keys_all_keys_exists(self):
        keys_list = ('language', 'username', 'password')
        creds = {
            'language': 'UA',
            'username': 'user',
            'password': 'pass'
        }
        self.assertTrue(validate_object_keys(keys_list, creds))

    def test_validate_object_keys_raise_exception_with_wrong_key(self):
        keys_list = ('language', 'username', 'password')
        creds = {
            'language': 'UA',
            'username': 'user',
            'nopassword': 'pass'
        }
        with self.assertRaises(Exception) as ke:
            validate_object_keys(keys_list, creds)
        self.assertEqual('Key is missing', str(ke.exception))

    @patch('smarsy.parse.open_json_file')
    def test_user_headers_object_is_the_same_like_in_file(self,
                                                          mock_json_load):
        expected = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
        mock_json_load.return_value = expected
        actual = get_headers()
        self.assertEqual(actual, expected)


@patch('smarsy.parse.perform_post_request', return_value='Smarsy Login')
@patch('smarsy.parse.get_user_credentials', return_value={'u': 'name'})
@patch('smarsy.parse.get_headers', return_value={'h': '123'})
class TestsParse(unittest.TestCase):
    def test_login_gets_headers(self,
                                mock_headers,
                                user_credentials,
                                mock_request):
        login()
        self.assertTrue(mock_headers.called)

    def test_login_gets_credentials(self,
                                    mock_headers,
                                    user_credentials,
                                    mock_request):
        login()
        self.assertTrue(user_credentials.called)

    @patch('requests.Session', return_value='session')
    def test_login_uses_login_page_in_request(self,
                                              mock_session,
                                              mock_headers,
                                              user_credentials,
                                              mock_request):
        login()
        mock_request.assert_called_with(mock_session.return_value,
                                        Urls.LOGIN.value,
                                        user_credentials.return_value,
                                        mock_headers.return_value)

    @patch('requests.Session', return_value='session')
    def test_login_returns_post_request_text(self,
                                             mock_session,
                                             mock_headers,
                                             user_credentials,
                                             mock_request):
        self.assertEqual(login(), 'Smarsy Login')

    def test_if_empty_keys_raise_exception_with_empty_key(self,
                                                          mock_headers,
                                                          user_credentials,
                                                          mock_request):
        keys_list = ()
        creds = {
            'language': 'UA',
            'username': 'user',
            'nopassword': 'pass'
        }
        with self.assertRaises(Exception) as ke:
            validate_object_keys(keys_list, creds)
        self.assertEqual('Key is empty', str(ke.exception))


class TestPageContent(unittest.TestCase):

    def test_login_page_has_expected_title(self):
        html = '<html><title>Smarsy - Смарсі - Україна</title></html>'
        actual = validate_title(html)
        self.assertTrue(actual)


if __name__ == '__main__':
    if '--unittest' in sys.argv:
        subprocess.call([sys.executable, '-m', 'unittest', 'discover'])
