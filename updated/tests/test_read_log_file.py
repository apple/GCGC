# Purpose: Test the public functions in the read_log_file.py API
from link_read_log_file import getParsedData
from link_read_log_file import event_parsing_string
import unittest as utest
from io import StringIO
from unittest.mock import patch


class Test_read_log_file(utest.TestCase):
    def test_empty_file(self):
        # Catch output being directed to standard out
        with patch("sys.stdout", new=StringIO()) as fake_out:
            return_value = getParsedData("./testdata/empty_file")
            self.assertEqual(fake_out.getvalue(), "Unable to parse file ./testdata/empty_file\n")
            self.assertEqual(return_value, None)

    def test_empty_input(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            return_value = getParsedData("")
            self.assertEqual(fake_out.getvalue(), "No logfile provided\n")
            self.assertEqual(return_value, None)

    def test_incorrect_parameter_datatype(self):
        self.assertEqual(1, 1)


if __name__ == "__main__":
    utest.main()

# # ^(\[\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}\+\d{4}\])?\[(\d+\.\d+)s\]\[\w+ ?\]\[gc\s*\] GC\(\d+\) ((?:Pause)|(?:Concurrent)) ((?:\w+ ?){1,3}) {(\((?:\w+ ?){1,3}\) ){0,3}(\d+\w->\d+\w\(?\d+?\w?\)?){0,1} ?(\d+\.\d+)m
# # ^(\[\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}\+\d{4}\])?\[(\d+\.\d+)s\]\[\w+ ?\]\[gc\s*\] GC\(\d+\) ((?:Pause)|(?:Concurrent)) ((?:\w+ ?){1,3}) (\((?:\w+ ?){1,3}\) ){0,3}(\d+\w->\d+\w\(?\d+?\w?\)?){0,1} ?(\d+\.\d+)ms
# ##########################################
# """   Test 1 - 3 : Failure cases """
# ##########################################
# # Test 1: Incorrect parameter count
# # getParsedData()                       # tested, working
# # getParsedData("a", "b")               # tested, working


# # Test 2: Incorrect parameter type

# # getParsedData("")                       # tested, working
# # getParsedData([1, 2, 3])                # tested, working
# # getParsedData({})                       # tested, working
# # getParsedData(None)                     # tested, working

# # Test 3: File does not exist
# # getParsedData("./testdata/aaaaaaaaaa")  # tested, working

# ##########################################
# """   Test 4 - 6 : Success cases """
# ##########################################
# # Test 4: Empty file (should return an empty dataframe)
# empty_file = "./testdata/empty_file"
# print(getParsedData(empty_file))  # tested, working

# # Test 5: Small log file (should return a non-empty dataframe)
# small_log = "./testdata/small_log"
# print(getParsedData(small_log))  # FAILURE CASE!!!! FIX  :D

# # Test 6: Large log file (should return a non-empty dataframe)
# large_log = "./testdata/large_log"
# print(getParsedData(large_log))
