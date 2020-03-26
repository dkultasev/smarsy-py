import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from pytest_mock import mocker 

from src import database

def test_db_connect_function_exists(mocker):
  mocker.patch.object(database, 'db_connect') 
