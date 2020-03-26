import os
import sys
import pytest
from pytest_mock import mocker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import database


def test_db_connect_function_exists(mocker):
    mocker.patch.object(database, 'db_connect')
