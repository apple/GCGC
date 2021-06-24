import pandas
import unittest as utest
from io import StringIO
from unittest.mock import patch
import sys

# How to test file: python3 -m unittest -v test_read_log_file.py

sys.path.append("/Users/ellisbrown/Desktop/Project/updated/src/")
import transform
from read_log_file import get_parsed_data_from_file

# Important files required for testing
empty_file = "./testdata/empty_file"
small_log = "./testdata/small_log"
large_log = "./testdata/large_log"
manual_log = "./testdata/manual_log"


class Test_sget_time_and_event_durations(utest.TestCase):
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


class Test_get_event_durations_in_miliseconds(utest.TestCase):
    def test_correct_parameters(self):
        self.assertRaises(AssertionError, transform.get_event_durations_in_miliseconds, 0)
        self.assertRaises(AssertionError, transform.get_event_durations_in_miliseconds, 100)
        self.assertRaises(AssertionError, transform.get_event_durations_in_miliseconds, {})
        self.assertRaises(AssertionError, transform.get_event_durations_in_miliseconds, {"Hello": "World"})
        self.assertRaises(AssertionError, transform.get_event_durations_in_miliseconds, [])
        self.assertRaises(AssertionError, transform.get_event_durations_in_miliseconds, [200, "Yes!"])
        self.assertRaises(AssertionError, transform.get_event_durations_in_miliseconds, "String")
        self.assertRaises(AssertionError, transform.get_event_durations_in_miliseconds, [[], []])

    def test_non_empty_case(self):
        data = get_parsed_data_from_file(small_log)
        a = transform.get_event_durations_in_miliseconds(data)
        self.assertNotEqual(a, [])

    def test_empty_case(self):
        a = transform.get_event_durations_in_miliseconds(pandas.DataFrame())
        self.assertEqual(a, [])


class Test_get_time_in_seconds(utest.TestCase):
    def test_correct_parameters(self):
        self.assertRaises(AssertionError, transform.get_time_in_seconds, 0)
        self.assertRaises(AssertionError, transform.get_time_in_seconds, 100)
        self.assertRaises(AssertionError, transform.get_time_in_seconds, {})
        self.assertRaises(AssertionError, transform.get_time_in_seconds, {"Hello": "World"})
        self.assertRaises(AssertionError, transform.get_time_in_seconds, [])
        self.assertRaises(AssertionError, transform.get_time_in_seconds, [200, "Yes!"])
        self.assertRaises(AssertionError, transform.get_time_in_seconds, "String")
        self.assertRaises(AssertionError, transform.get_time_in_seconds, [[], []])

    def test_non_empty_case(self):
        data = get_parsed_data_from_file(small_log)
        a = transform.get_time_in_seconds(data)
        self.assertNotEqual(a, [])

    def test_empty_case(self):
        a = transform.get_time_in_seconds(pandas.DataFrame())
        self.assertEqual(a, [])


if __name__ == "__main__":
    utest.main()
