import unittest
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..', 'smarsy')))
# excluding following line for linter as it complains that
# from import is supposed to be at the top of the file

from smarsy.bs_helper import BSHelper # noqa


class TestBSHelperInstance(unittest.TestCase):
    def setUp(self):
        self.html = 'some html'
        self.source_page = BSHelper(self.html)

    def test_bshelper_instance_created(self):
        self.assertEqual(self.source_page.html, self.html)
