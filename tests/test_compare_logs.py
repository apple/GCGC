# Testing for the file compare_logs.py
from ast import parse
from numpy import empty, select
import pandas
import unittest as utest
from io import StringIO
from unittest.mock import patch
import sys

# How to test file: python3 -m unittest -v test_compare_logs.py

sys.path.append("../src")
import transform
from read_log_file import get_parsed_data_from_file

# Important files required for testing
empty_file = "./testdata/empty_file"
small_log = "./testdata/small_log"
large_log = "./testdata/large_log"
manual_log = "./testdata/manual_log"

from compare_logs import get_parsed_comparions_from_files


class Test_get_parsed_comparions_from_files(utest.TestCase):

    files = [empty_file, small_log, large_log, manual_log]

    # Tests that the data types of parameters must be correct.
    def test_correct_parametertype(self):
        self.assertRaises(AssertionError, get_parsed_comparions_from_files, 0)
        self.assertRaises(AssertionError, get_parsed_comparions_from_files, 100)
        self.assertRaises(AssertionError, get_parsed_comparions_from_files, {})
        self.assertRaises(AssertionError, get_parsed_comparions_from_files, {"Hello": "World"})
        self.assertRaises(AssertionError, get_parsed_comparions_from_files, [200, "Yes!"])
        self.assertRaises(AssertionError, get_parsed_comparions_from_files, "String")
        # List is the expected data type, but an empyu list should raise a warning
        with patch("sys.stdout", new=StringIO()) as fake_out:
            data = get_parsed_comparions_from_files([])
            self.assertEqual(data, [])
            self.assertEqual(fake_out.getvalue(), "Warning: Files list empty in get_parsed_comparions_from_files\n")

        # List with nested empty values should raise a value when parsing the empty values.
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.assertRaises(AssertionError, get_parsed_comparions_from_files, [[], []])

    # Test when the parameters are correct, but contain an empty data set.
    def test_empty_case(self):
        # Parse a list containing filenames of only data, then check if the data returned is an emppty panda DF.
        gc_event_tables = get_parsed_comparions_from_files([empty_file])
        self.assertEqual(gc_event_tables, [pandas.DataFrame()])
        with patch("sys.stdout", new=StringIO()) as fake_out:
            gc_event_tables = get_parsed_comparions_from_files([empty_file])
            self.assertEqual(gc_event_tables, [pandas.DataFrame()])
            self.assertEqual(fake_out.getvalue(), "Unable to parse file " + empty_file + "\n")

    def test_non_empty_case(self):
        data = get_parsed_comparions_from_files(small_log)
        a, b = get_parsed_comparions_from_files(data)
        self.assertNotEqual(a, [])
        self.assertNotEqual(b, [])
