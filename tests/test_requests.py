from unittest.mock import patch, Mock

import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..',
                                             'smarsy')))
# excluding following line for linter as it complains that
# from import is supposed to be at the top of the file
from smarsy.parse import (perform_get_request, perform_post_request)  # noqa


class Test_http_requests(unittest.TestCase):
    @classmethod
    @patch('requests.Session')
    def setUpClass(cls, mocked_session):
        cls.mocked_session = mocked_session
        cls.default_url = 'http://www.smarsy.ua'
        cls.default_text = 'Informative text'
        cls.default_status_code = 200
        cls.mocked_session.get.return_value = Mock(
            status_code=cls.default_status_code,
            text=cls.default_text)
        cls.mocked_session.post.return_value = Mock(
            status_code=cls.default_status_code,
            text=cls.default_text)


class Test_perform_get_request(Test_http_requests):
    def setUp(self):
        self.mocked_session.get.return_value.status_code = (
            self.default_status_code)

    def test_request_get_method_is_called_with_providen_url(
            self):
        perform_get_request(self.mocked_session, self.default_url)
        self.mocked_session.get.assert_called_with(url=self.default_url,
                                                   params=None, headers=None)

    def test_request_get_method_is_called_with_providen_params(
            self):
        expected_params = 'params'
        perform_get_request(self.mocked_session, self.default_url,
                            params=expected_params)
        self.mocked_session.get.assert_called_with(url=self.default_url,
                                                   params=expected_params,
                                                   headers=None)

    def test_request_get_method_is_called_with_providen_headers(
            self):
        expected_headers = {"a": 1}
        perform_get_request(self.mocked_session, self.default_url,
                            headers=expected_headers)
        self.mocked_session.get.assert_called_with(url=self.default_url,
                                                   params=None,
                                                   headers=expected_headers)

    def test_request_text_is_returned_as_function_output(
            self):
        expected_text = 'some_text'
        self.mocked_session.get(self.default_url).text = expected_text
        self.assertEqual(perform_get_request(self.mocked_session,
                                             self.default_url),
                         expected_text)

    @patch('requests.HTTPError', Exception)
    def test_response_with_status_code_404_raises_exception(
            self):
        self.mocked_session.get.return_value.status_code = 404
        self.assertRaises(Exception, perform_get_request,
                          self.mocked_session, self.default_url)


class Test_perform_post_request(Test_http_requests):
    def setUp(self):
        self.mocked_session.post.return_value.status_code = (
            self.default_status_code)

    def test_request_post_method_is_called_with_providen_url(
            self):
        perform_post_request(self.mocked_session, self.default_url)
        self.mocked_session.post.assert_called_with(url=self.default_url,
                                                    data=None, headers=None)

    def test_request_post_method_is_called_with_providen_data(
            self):
        expected_data = 'data'
        perform_post_request(self.mocked_session, self.default_url,
                             data=expected_data)
        self.mocked_session.post.assert_called_with(url=self.default_url,
                                                    data=expected_data,
                                                    headers=None)

    def test_request_get_method_is_called_with_providen_headers(
            self):
        expected_headers = {"a": 1}
        perform_post_request(self.mocked_session, self.default_url,
                             headers=expected_headers)
        self.mocked_session.post.assert_called_with(url=self.default_url,
                                                    data=None,
                                                    headers=expected_headers)

    def test_request_get_method_is_called_with_providen_encoding(self):
        expected_encoding = 'utf8'
        perform_post_request(self.mocked_session, self.default_url,
                             encoding=expected_encoding)
        self.assertEqual(self.mocked_session.post.return_value.encoding,
                         expected_encoding)

    def test_request_text_is_returned_as_function_output(
            self):
        expected_text = 'some_text'
        self.mocked_session.post(self.default_url).text = expected_text
        self.assertEqual(perform_post_request(self.mocked_session,
                                              self.default_url),
                         expected_text)

    @patch('requests.HTTPError', Exception)
    def test_response_with_status_code_404_raises_exception(
            self):
        self.mocked_session.post.return_value.status_code = 404
        self.assertRaises(Exception, perform_post_request,
                          self.mocked_session, self.default_url)
