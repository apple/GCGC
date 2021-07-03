from ast import parse
from numpy import select
import pandas
import unittest as utest
from io import StringIO
from unittest.mock import patch
import sys

# How to test file: python3 -m unittest -v test_transform.py

sys.path.append("../src")
import transform
from read_log_file import get_parsed_data_from_file

# Important files required for testing
empty_file = "./testdata/empty_file"
small_log = "./testdata/small_log"
large_log = "./testdata/large_log"
manual_log = "./testdata/manual_log"


class Test_get_time_and_event_durations(utest.TestCase):
    def test_correct_parametertype(self):
        self.assertRaises(AssertionError, transform.get_time_and_event_durations, 0)
        self.assertRaises(AssertionError, transform.get_time_and_event_durations, 100)
        self.assertRaises(AssertionError, transform.get_time_and_event_durations, {})
        self.assertRaises(AssertionError, transform.get_time_and_event_durations, {"Hello": "World"})
        self.assertRaises(AssertionError, transform.get_time_and_event_durations, [])
        self.assertRaises(AssertionError, transform.get_time_and_event_durations, [200, "Yes!"])
        self.assertRaises(AssertionError, transform.get_time_and_event_durations, "String")
        self.assertRaises(AssertionError, transform.get_time_and_event_durations, [[], []])

    def test_non_empty_case(self):
        data = get_parsed_data_from_file(small_log)
        a, b = transform.get_time_and_event_durations(data)
        self.assertNotEqual(a, [])
        self.assertNotEqual(b, [])

    def test_empty_case(self):
        a, b = transform.get_time_and_event_durations(pandas.DataFrame())
        self.assertEqual(a, [])
        self.assertEqual(b, [])
