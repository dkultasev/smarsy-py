import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..',
                                             'smarsy')))
# excluding following line for linter as it complains that
# from import is supposed to be at the top of the file

from smarsy.parse import Person # noqa


class TestPersonClass(unittest.TestCase):
    def test_person_instance_created(self):
        person = Person('Вася', 'Пупкин', 'Иванович', 'Деда', '30-02-2000')
        self.assertEqual(person.first_name, 'Вася')
        self.assertEqual(person.second_name, 'Пупкин')
        self.assertEqual(person.middle_name, 'Иванович')
        self.assertEqual(person.person_type, 'Деда')
        self.assertEqual(person.birth_date, '30-02-2000')
