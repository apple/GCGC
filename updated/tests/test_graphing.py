from numpy import select
import pandas
import unittest as utest
from io import StringIO
from unittest.mock import patch
import sys

# How to test file: python3 -m unittest -v test_graphing.py

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


class Test_get_times_and_durations_from_event_lists(utest.TestCase):
    def test_correct_parameters(self):
        self.assertRaises(AssertionError, transform.get_times_and_durations_from_event_lists, 0)
        self.assertRaises(AssertionError, transform.get_times_and_durations_from_event_lists, 100)
        self.assertRaises(AssertionError, transform.get_times_and_durations_from_event_lists, {})
        self.assertRaises(AssertionError, transform.get_times_and_durations_from_event_lists, {"Hello": "World"})
        self.assertRaises(AssertionError, transform.get_times_and_durations_from_event_lists, [200, "Yes!"])
        self.assertRaises(AssertionError, transform.get_times_and_durations_from_event_lists, "String")
        self.assertRaises(AssertionError, transform.get_times_and_durations_from_event_lists, [[], []])

    def test_non_empty_case(self):
        data = get_parsed_data_from_file(small_log)
        pauses, concurrent = transform.seperatePausesConcurrent(data)
        a, b = transform.get_times_and_durations_from_event_lists([pauses, concurrent])
        self.assertNotEqual(a, [])
        self.assertNotEqual(b, [])

    def test_empty_case(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            a, b = transform.get_times_and_durations_from_event_lists([])
            self.assertEqual(fake_out.getvalue(), "Error: event_tables empty\n")
            self.assertEqual(a, [])
            self.assertEqual(b, [])


class Test_get_event_table_labels(utest.TestCase):
    def test_correct_parameters(self):
        self.assertRaises(AssertionError, transform.get_event_table_labels, 0)
        self.assertRaises(AssertionError, transform.get_event_table_labels, 100)
        self.assertRaises(AssertionError, transform.get_event_table_labels, {})
        self.assertRaises(AssertionError, transform.get_event_table_labels, {"Hello": "World"})
        self.assertRaises(AssertionError, transform.get_event_table_labels, [200, "Yes!"])
        self.assertRaises(AssertionError, transform.get_event_table_labels, "String")
        self.assertRaises(AssertionError, transform.get_event_table_labels, [[], []])

    def test_empty_case(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            result = transform.get_event_table_labels([], True)
            self.assertEqual(None, result)
            self.assertEqual(fake_out.getvalue(), "Error: event_tables empty\n")

    def test_non_empty_case(self):
        data = get_parsed_data_from_file(small_log)
        stw, con = transform.seperatePausesConcurrent(data)
        result = transform.get_event_table_labels([stw])
        self.assertNotEqual(result, [])
        self.assertEqual(result[0], "Pause Young")
        result = transform.get_event_table_labels([stw], False)
        self.assertNotEqual(result, [])
        self.assertEqual(result[0], "Young")

        with patch("sys.stdout", new=StringIO()) as fake_out:
            data = get_parsed_data_from_file(small_log)
            stw, con = transform.seperatePausesConcurrent(data)
            result = transform.get_event_table_labels([stw, con])
            self.assertEqual(result, [])
            self.assertEqual(fake_out.getvalue(), "Error: Empty table in event_table, unable to assign it a label\n")


class Test_compare_eventtype_time_sums(utest.TestCase):
    def test_correct_parameters(self):
        self.assertRaises(AssertionError, transform.compare_eventtype_time_sums, 0)
        self.assertRaises(AssertionError, transform.compare_eventtype_time_sums, 100)
        self.assertRaises(AssertionError, transform.compare_eventtype_time_sums, {})
        self.assertRaises(AssertionError, transform.compare_eventtype_time_sums, {"Hello": "World"})
        self.assertRaises(AssertionError, transform.compare_eventtype_time_sums, [200, "Yes!"])
        self.assertRaises(AssertionError, transform.compare_eventtype_time_sums, "String")
        self.assertRaises(AssertionError, transform.compare_eventtype_time_sums, [[], []])

    def test_empty_case(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            result = transform.compare_eventtype_time_sums(pandas.DataFrame())
            self.assertEqual(result, (0, 0))
            self.assertEqual(fake_out.getvalue(), "Error: Database_table is empty\n")

    def test_non_empty_case(self):
        data = get_parsed_data_from_file(small_log)
        a, b = transform.compare_eventtype_time_sums(data)
        self.assertNotEqual(a, 0)  # there are young pauses
        self.assertEqual(b, 0)  # there are no concurrent periods in the dataset.


class Test_get_concurrent_data(utest.TestCase):
    def test_correct_parameters(self):
        self.assertRaises(AssertionError, transform.get_concurrent_data, 0)
        self.assertRaises(AssertionError, transform.get_concurrent_data, 100)
        self.assertRaises(AssertionError, transform.get_concurrent_data, {})
        self.assertRaises(AssertionError, transform.get_concurrent_data, {"Hello": "World"})
        self.assertRaises(AssertionError, transform.get_concurrent_data, [200, "Yes!"])
        self.assertRaises(AssertionError, transform.get_concurrent_data, "String")
        self.assertRaises(AssertionError, transform.get_concurrent_data, [[], []])
    
    def test_empty_case(self):
        


if __name__ == "__main__":
    utest.main()
