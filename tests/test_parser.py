import os
import sys
import unittest
# from src import parse.get_credentials

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class Tests_Login(unittest.TestCase):

    def test_read_credentials_from_file(self):


    def test_get_user_credentials(self):
        expected_creds = {'login': 'user', 'password': ''}
        actual_creds = get_credentials()
        self.assertEqual(expected_creds, actual_creds)


if __name__ == "__main__":
    unittest.main()
