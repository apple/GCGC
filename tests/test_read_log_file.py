# Purpose: Test the public functions in the read_log_file.py API
# Ellis Brown
# 6/23/2021
# How to test file: python3 -m unittest -v test_read_log_file.py
import pandas
import unittest as utest
from io import StringIO
from unittest.mock import patch
import sys

sys.path.append("/Users/ellisbrown/Desktop/Project/updated/src/")
from read_log_file import get_parsed_data_from_file


# Important files required for testing
empty_file = "./testdata/empty_file"
small_log = "./testdata/small_log"
large_log = "./testdata/large_log"
manual_log = "./testdata/manual_log"


class Test_read_log_file(utest.TestCase):
    def test_empty_file(self):
        # Catch output being directed to standard out
        with patch("sys.stdout", new=StringIO()) as fake_out:
            return_value = get_parsed_data_from_file(empty_file)
            self.assertEqual(fake_out.getvalue(), "Unable to parse file ./testdata/empty_file\n")
            self.assertEqual(return_value, None)

    def test_empty_input(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            return_value = get_parsed_data_from_file("")
            self.assertEqual(fake_out.getvalue(), "No logfile provided\n")
            self.assertEqual(return_value, None)

    # Test to make sure that the only parameter input type can be a string
    def test_incorrect_parameter_datatype(self):
        self.assertRaises(AssertionError, get_parsed_data_from_file, 200)
        self.assertRaises(AssertionError, get_parsed_data_from_file, {"Name": "Pokemon"})
        self.assertRaises(AssertionError, get_parsed_data_from_file, {})
        self.assertRaises(AssertionError, get_parsed_data_from_file, 0)
        self.assertRaises(AssertionError, get_parsed_data_from_file, {"apple"})
        self.assertRaises(AssertionError, get_parsed_data_from_file, False)
        self.assertRaises(AssertionError, get_parsed_data_from_file, True)
        self.assertRaises(AssertionError, get_parsed_data_from_file, (1, 2, 3))
        self.assertRaises(AssertionError, get_parsed_data_from_file, [])

    # Confirm that correctly populated log files return the correct data types
    def test_data_types_return(self):
        self.assertTrue(isinstance(get_parsed_data_from_file(small_log), pandas.DataFrame))
        self.assertTrue(isinstance(get_parsed_data_from_file(small_log), pandas.DataFrame))
        self.assertFalse(get_parsed_data_from_file(small_log).empty)
        self.assertFalse(get_parsed_data_from_file(large_log).empty)

    # Verify the columns returned from a successful parsing are correct
    def test_column_names(self):
        returned_data = get_parsed_data_from_file(small_log)
        self.assertEqual(
            list(returned_data.columns),
            [
                "DateTime",
                "TimeFromStart_seconds",
                "EventType",
                "EventName",
                "AdditionalEventInfo",
                "MemoryChange_MB",
                "Duration_miliseconds",
            ],
        )


if __name__ == "__main__":
    utest.main()
