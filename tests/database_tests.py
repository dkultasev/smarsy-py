import os
import sys

# add 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), '..'), 'src')))


import mock 
import pytest
from pytest_mock import mocker 

import database

import mysql.connector as mysql

def test_db_connect(mocker):
  mocker.patch.object(database, 'db_connect') 