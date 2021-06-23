# Purpose: Test the public functions in the read_log_file.py API
from link_read_log_file import getParsedData
from link_read_log_file import event_parsing_string
import pandas
import unittest as utest
from io import StringIO
from unittest.mock import patch

# How to test file: python3 -m unittest -v test_read_log_file.py
#                                       ^ optional parameter

# Important files required for testing
empty_file = "./testdata/empty_file"
small_log = "./testdata/small_log"
large_log = "./testdata/large_log"
manual_log = "./testdata/manual_log"


class Test_read_log_file(utest.TestCase):
    def test_empty_file(self):
        # Catch output being directed to standard out
        with patch("sys.stdout", new=StringIO()) as fake_out:
            return_value = getParsedData(empty_file)
            self.assertEqual(fake_out.getvalue(), "Unable to parse file ./testdata/empty_file\n")
            self.assertEqual(return_value, None)

    def test_empty_input(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            return_value = getParsedData("")
            self.assertEqual(fake_out.getvalue(), "No logfile provided\n")
            self.assertEqual(return_value, None)

    # Test to make sure that the only parameter input type can be a string
    def test_incorrect_parameter_datatype(self):
        self.assertRaises(AssertionError, getParsedData, 200)
        self.assertRaises(AssertionError, getParsedData, {"Name": "Pokemon"})
        self.assertRaises(AssertionError, getParsedData, {})
        self.assertRaises(AssertionError, getParsedData, 0)
        self.assertRaises(AssertionError, getParsedData, {"apple"})
        self.assertRaises(AssertionError, getParsedData, False)
        self.assertRaises(AssertionError, getParsedData, True)
        self.assertRaises(AssertionError, getParsedData, (1, 2, 3))
        self.assertRaises(AssertionError, getParsedData, [])

    # Confirm that correctly populated log files return the correct data types
    def test_data_types_return(self):
        self.assertTrue(isinstance(getParsedData(small_log), pandas.DataFrame))
        self.assertTrue(isinstance(getParsedData(small_log), pandas.DataFrame))
        self.assertFalse(getParsedData(small_log).empty)
        self.assertFalse(getParsedData(large_log).empty)

    def test_column_names(self):
        returned_data = getParsedData(small_log)
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

    def test_returned_values(self):
        returned_data = getParsedData(manual_log)
        data = [
            [None, "1.042", "Pause", "Young", "(Normal) (G1 Evacuation Pause) ", "108M->59M(1040M)", 10.421],
            [None, 0.070, "Pause", "Init Mark", "(unload classes) ", None, 0.160],
            [
                "2020-11-16T15:49:20.881+0000",
                3304.479,
                "Pause",
                "Young",
                "(Normal) (G1 Evacuation Pause)",
                "8287M->3649M(12000M)",
                132.704,
            ],
        ]
        columns = [
            "DateTime",
            "TimeFromStart_seconds",
            "EventType",
            "EventName",
            "AdditionalEventInfo",
            "MemoryChange_MB",
            "Duration_miliseconds",
        ]
        df = pandas.DataFrame(data)
        df.columns = columns
        print(df)
        print(returned_data)
        new_df = returned_data.eq(df)
        print(new_df)
        self.assertTrue(returned_data.eq(df).all())


if __name__ == "__main__":
    utest.main()
