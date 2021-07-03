import pandas
import unittest as utest
from io import StringIO
from unittest.mock import patch
import sys

# Test using: python3 -m unittest -v test_graphing.py
sys.path.append("../src")
import graphing as graph
from transform import compare_eventtype_time_sums


# Important files required for testing
empty_file = "./testdata/empty_file"
small_log = "./testdata/small_log"
large_log = "./testdata/large_log"
manual_log = "./testdata/manual_log"


# class Test_compare_eventtypes_pie(utest.TestCase):
#     def test_incorrect_parameter_type(self):
#         self.assertRaises(AssertionError, graph.compare_eventtypes.wcompare_eventtypes_pie, [])
#         self.assertRaises(AssertionError, graph.compare_eventtypes_pie, ["non empty"])
#         self.assertRaises(AssertionError, graph.compare_eventtypes_pie, {})
#         self.assertRaises(AssertionError, graph.compare_eventtypes_pie, {"Test": 0})
#         self.assertRaises(AssertionError, graph.compare_eventtypes_pie, "")
#         self.assertRaises(AssertionError, graph.compare_eventtypes_pie, "str")
#         self.assertRaises(AssertionError, graph.compare_eventtypes_pie, 0)
#         self.assertRaises(AssertionError, graph.compare_eventtypes_pie, 1)
#         self.assertRaises(AssertionError, graph.compare_eventtypes_pie, (1, 2))
#         self.assertRaises(AssertionError, graph.compare_eventtypes_pie, tuple())
#         self.assertRaises(AssertionError, graph.compare_eventtypes_pie, False)
#         self.assertRaises(AssertionError, graph.compare_eventtypes_pie, True)

#     def test_empty_database(self):
#         with patch("sys.stdout", new=StringIO()) as fake_out:
#             return_value = graph.compare_eventtypes_pie(pandas.DataFrame())
#             self.assertEqual(fake_out.getvalue(), "Error: Empty database_dable in compare_eventtypes_pie\n")
#             self.assertEqual(return_value, None)
