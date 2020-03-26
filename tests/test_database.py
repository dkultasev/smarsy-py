import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest

from src import database

class Tests_Login(unittest.TestCase):
  def test_get_user_credentials(self):
    print('a')