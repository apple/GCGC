from ast import parse
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
        pauses, concurrent = transform.seperate_pauses_concurrent(data)
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
        stw, con = transform.seperate_pauses_concurrent(data)
        result = transform.get_event_table_labels([stw])
        self.assertNotEqual(result, [])
        self.assertEqual(result[0], "Pause Young")
        result = transform.get_event_table_labels([stw], False)
        self.assertNotEqual(result, [])
        self.assertEqual(result[0], "Young")

        with patch("sys.stdout", new=StringIO()) as fake_out:
            data = get_parsed_data_from_file(small_log)
            stw, con = transform.seperate_pauses_concurrent(data)
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
        with patch("sys.stdout", new=StringIO()) as fake_out:
            result = transform.get_concurrent_data(pandas.DataFrame())
            self.assertEqual(result, None)
            self.assertEqual(fake_out.getvalue(), "Warning: Empty database table in get_concurrent_data\n")

    def test_non_empty_case(self):
        data = get_parsed_data_from_file(large_log)
        result = transform.get_concurrent_data(data)
        for line in result["EventType"]:
            # test that the outputs are correct.
            self.assertEqual(line, "Concurrent")


class Test_get_pauses_data(utest.TestCase):
    def test_correct_parameters(self):
        self.assertRaises(AssertionError, transform.get_pauses_data, 0)
        self.assertRaises(AssertionError, transform.get_pauses_data, 100)
        self.assertRaises(AssertionError, transform.get_pauses_data, {})
        self.assertRaises(AssertionError, transform.get_pauses_data, {"Hello": "World"})
        self.assertRaises(AssertionError, transform.get_pauses_data, [200, "Yes!"])
        self.assertRaises(AssertionError, transform.get_pauses_data, "String")
        self.assertRaises(AssertionError, transform.get_pauses_data, [[], []])

    def test_empty_case(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            result = transform.get_pauses_data(pandas.DataFrame())
            self.assertEqual(result, None)
            self.assertEqual(fake_out.getvalue(), "Warning: Empty database table in get_pauses_data\n")

    def test_non_empty_case(self):
        data = get_parsed_data_from_file(large_log)
        result = transform.get_pauses_data(data)
        for line in result["EventType"]:
            # test that the outputs are correct.
            self.assertEqual(line, "Pause")


class Test_seperate_pauses_concurrent(utest.TestCase):
    def test_correct_parameters(self):
        self.assertRaises(AssertionError, transform.seperate_pauses_concurrent, 0)
        self.assertRaises(AssertionError, transform.seperate_pauses_concurrent, 100)
        self.assertRaises(AssertionError, transform.seperate_pauses_concurrent, {})
        self.assertRaises(AssertionError, transform.seperate_pauses_concurrent, {"Hello": "World"})
        self.assertRaises(AssertionError, transform.seperate_pauses_concurrent, [200, "Yes!"])
        self.assertRaises(AssertionError, transform.seperate_pauses_concurrent, "String")
        self.assertRaises(AssertionError, transform.seperate_pauses_concurrent, [[], []])

    def test_empty_case(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            result = transform.seperate_pauses_concurrent(pandas.DataFrame())
            self.assertEqual(result, None)
            self.assertEqual(fake_out.getvalue(), "Warning: Empty database table in seperate_pauses_concurrent\n")

    def test_non_empty_case(self):
        data = get_parsed_data_from_file(large_log)
        pauses, concurrent = transform.seperate_pauses_concurrent(data)
        for line in pauses["EventType"]:
            # test that the outputs are correct.
            self.assertEqual(line, "Pause")

        for line in concurrent["EventType"]:
            # test that the outputs are correct.
            self.assertEqual(line, "Concurrent")


class Test_seperate_by_event_name(utest.TestCase):
    def test_correct_parameters(self):
        self.assertRaises(AssertionError, transform.seperate_by_event_name, 0)
        self.assertRaises(AssertionError, transform.seperate_by_event_name, 100)
        self.assertRaises(AssertionError, transform.seperate_by_event_name, {})
        self.assertRaises(AssertionError, transform.seperate_by_event_name, {"Hello": "World"})
        self.assertRaises(AssertionError, transform.seperate_by_event_name, [200, "Yes!"])
        self.assertRaises(AssertionError, transform.seperate_by_event_name, "String")
        self.assertRaises(AssertionError, transform.seperate_by_event_name, [[], []])

    def test_empty_case(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            result = transform.seperate_by_event_name(pandas.DataFrame())
            self.assertEqual(result, None)
            self.assertEqual(fake_out.getvalue(), "Warning: Empty database table in seperate_by_event_name\n")

    # Note: this one deviates from the typical pattern
    def test_non_empty_case(self):
        data = get_parsed_data_from_file(large_log)
        list_of_tables = transform.seperate_by_event_name(data)
        names = {}
        for table in list_of_tables:
            # Confirm all EventNames in this share the same name.
            # Then confirm this is the only table with the name.
            unique_name = ""
            unique_name = table["EventName"].iloc[0]
            for name in table["EventName"]:
                self.assertEqual(unique_name, name)

            self.assertTrue(name not in names)
            names[name] = 0


class Test_get_heap_occupancy(utest.TestCase):
    def test_correct_parameters(self):
        self.assertRaises(AssertionError, transform.get_heap_occupancy, 0)
        self.assertRaises(AssertionError, transform.get_heap_occupancy, 100)
        self.assertRaises(AssertionError, transform.get_heap_occupancy, {})
        self.assertRaises(AssertionError, transform.get_heap_occupancy, {"Hello": "World"})
        self.assertRaises(AssertionError, transform.get_heap_occupancy, [200, "Yes!"])
        self.assertRaises(AssertionError, transform.get_heap_occupancy, "String")
        self.assertRaises(AssertionError, transform.get_heap_occupancy, [[], []])

    def test_empty_case(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            result = transform.get_heap_occupancy(pandas.DataFrame())
            self.assertEqual(result, None)
            self.assertEqual(fake_out.getvalue(), "Warning: Empty database_table in get_heap_occupancy\n")

    def test_non_empty_case(self):
        data = get_parsed_data_from_file(large_log)
        before_gc, after_gc, max_heap, parsed_timestamps = transform.get_heap_occupancy(data)
        self.assertEqual(len(before_gc), len(after_gc))
        self.assertEqual(len(max_heap), len(after_gc))
        self.assertEqual(len(parsed_timestamps), len(after_gc))
        self.assertTrue(before_gc and after_gc and max_heap and parsed_timestamps)
        self.assertIsInstance(before_gc, list)
        self.assertIsInstance(after_gc, list)
        self.assertIsInstance(max_heap, list)
        self.assertIsInstance(parsed_timestamps, list)
        self.assertTrue((type(before_gc[0]) == int) or (type(before_gc[0]) == float))
        self.assertTrue((type(after_gc[0]) == int) or (type(after_gc[0]) == float))
        self.assertTrue((type(max_heap[0]) == int) or (type(max_heap[0]) == float))
        self.assertTrue((type(parsed_timestamps[0]) == int) or (type(parsed_timestamps[0]) == float))


class Test_get_reclaimed_mb_over_time(utest.TestCase):
    def test_correct_parameters(self):
        self.assertRaises(AssertionError, transform.get_reclaimed_mb_over_time, 0)
        self.assertRaises(AssertionError, transform.get_reclaimed_mb_over_time, 100)
        self.assertRaises(AssertionError, transform.get_reclaimed_mb_over_time, {})
        self.assertRaises(AssertionError, transform.get_reclaimed_mb_over_time, {"Hello": "World"})
        self.assertRaises(AssertionError, transform.get_reclaimed_mb_over_time, [200, "Yes!"])
        self.assertRaises(AssertionError, transform.get_reclaimed_mb_over_time, "String")
        self.assertRaises(AssertionError, transform.get_reclaimed_mb_over_time, [[], []])

    def test_empty_case(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            reclaimed_bytes, timestamps = transform.get_reclaimed_mb_over_time(pandas.DataFrame())
            self.assertEqual(reclaimed_bytes, [])
            self.assertEqual(timestamps, [])
            self.assertEqual(
                fake_out.getvalue(),
                "Warning: Empty database_table in get_reclaimed_mb_over_time\n",
            )

    def test_non_empty_case(self):
        data = get_parsed_data_from_file(large_log)
        reclaimed, parsed_timestamps = transform.get_reclaimed_mb_over_time(data)
        self.assertEqual(len(reclaimed), len(parsed_timestamps))
        self.assertTrue(reclaimed and parsed_timestamps)
        self.assertTrue(reclaimed, list)
        self.assertTrue((type(reclaimed[0]) == int) or (type(reclaimed[0]) == float))
        self.assertTrue((type(parsed_timestamps[0]) == int) or (type(parsed_timestamps[0]) == float))


class Test_group_into_pause_buckets(utest.TestCase):
    def test_correct_parameters(self):
        self.assertRaises(AssertionError, transform.group_into_pause_buckets, 0, 5)
        self.assertRaises(AssertionError, transform.group_into_pause_buckets, 100, 5)
        self.assertRaises(AssertionError, transform.group_into_pause_buckets, {}, 5)
        self.assertRaises(AssertionError, transform.group_into_pause_buckets, {"Hello": "World"}, 5)
        self.assertRaises(AssertionError, transform.group_into_pause_buckets, [200, "Yes!"], 5)
        self.assertRaises(AssertionError, transform.group_into_pause_buckets, pandas.DataFrame(), [])
        self.assertRaises(AssertionError, transform.group_into_pause_buckets, pandas.DataFrame(), {})
        self.assertRaises(AssertionError, transform.group_into_pause_buckets, pandas.DataFrame(), "")
        self.assertRaises(AssertionError, transform.group_into_pause_buckets, pandas.DataFrame(), {"e": "e"})
        self.assertRaises(AssertionError, transform.group_into_pause_buckets, pandas.DataFrame(), [200, "Yes!"])
        self.assertRaises(AssertionError, transform.group_into_pause_buckets, pandas.DataFrame(), (1, 2))
        self.assertRaises(AssertionError, transform.group_into_pause_buckets, pandas.DataFrame(), [[], []])

    def test_empty_case(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            buckets = transform.group_into_pause_buckets(pandas.DataFrame(), 15)
            self.assertEqual(buckets, None)
            self.assertEqual(
                fake_out.getvalue(),
                "Warning: Empty table in group_into_pause_buckets.\n",
            )

    def test_zero_case(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            data = get_parsed_data_from_file(large_log)
            buckets = transform.group_into_pause_buckets(data, 0)
            self.assertEqual(buckets, None)
            self.assertEqual(
                fake_out.getvalue(),
                "Warning: Bucket_size_ms is equal to zero. Please use a positive number.\n",
            )

    def test_negative_case(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            data = get_parsed_data_from_file(large_log)
            buckets = transform.group_into_pause_buckets(data, -400)
            self.assertEqual(buckets, None)
            self.assertEqual(
                fake_out.getvalue(),
                "Warning: Bucket_size_ms is equal to zero. Please use a positive number.\n",
            )

    def test_non_empty_case(self):
        data = get_parsed_data_from_file(large_log)
        frequencies = transform.group_into_pause_buckets(data, 13.5)
        self.assertTrue(frequencies)
        frequencies = transform.group_into_pause_buckets(data, 4)
        self.assertTrue(frequencies)


class Test_get_heatmap_data(utest.TestCase):
    def test_correct_parameters(self):
        self.assertRaises(AssertionError, transform.get_heatmap_data, 0, 0, 0, 0, 0)
        self.assertRaises(AssertionError, transform.get_heatmap_data, [], "String!", 5, 5, 5)
        self.assertRaises(AssertionError, transform.get_heatmap_data, {}, 5, 10, 10, 10)
        self.assertRaises(AssertionError, transform.get_heatmap_data, (1, 2), 5, "String", 5, 5)

    def test_empty_case(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            buckets, dimensions = transform.get_heatmap_data(pandas.DataFrame(), 1, 1, 1, 1)
            self.assertEqual(buckets, None)
            self.assertEqual(dimensions, None)
            self.assertEqual(fake_out.getvalue(), "Warning: Empty table in get_heatmap_data.\n")

    def test_zero_case(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            data = get_parsed_data_from_file(large_log)
            buckets, dimensions = transform.get_heatmap_data(data, 0, 1, 1, 1)
            self.assertEqual(buckets, None)
            self.assertEqual(dimensions, None)
            self.assertEqual(fake_out.getvalue(), "Warning: All dimensions must be greater than zero.\n")
        with patch("sys.stdout", new=StringIO()) as fake_out:
            data = get_parsed_data_from_file(large_log)
            buckets, dimensions = transform.get_heatmap_data(data, 1, 0, 1, 1)
            self.assertEqual(buckets, None)
            self.assertEqual(dimensions, None)
            self.assertEqual(fake_out.getvalue(), "Warning: All dimensions must be greater than zero.\n")
        with patch("sys.stdout", new=StringIO()) as fake_out:
            data = get_parsed_data_from_file(large_log)
            buckets, dimensions = transform.get_heatmap_data(data, 1, 1, 0, 1)
            self.assertEqual(buckets, None)
            self.assertEqual(dimensions, None)
            self.assertEqual(fake_out.getvalue(), "Warning: All dimensions must be greater than zero.\n")
        with patch("sys.stdout", new=StringIO()) as fake_out:
            data = get_parsed_data_from_file(large_log)
            buckets, dimensions = transform.get_heatmap_data(data, 1, 1, 1, 0)
            self.assertEqual(buckets, None)
            self.assertEqual(dimensions, None)
            self.assertEqual(fake_out.getvalue(), "Warning: All dimensions must be greater than zero.\n")

    def test_negative_case(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            data = get_parsed_data_from_file(large_log)
            buckets, dimensions = transform.get_heatmap_data(data, 1, 1, 1, -1)
            self.assertEqual(buckets, None)
            self.assertEqual(dimensions, None)
            self.assertEqual(fake_out.getvalue(), "Warning: All dimensions must be greater than zero.\n")
        with patch("sys.stdout", new=StringIO()) as fake_out:
            data = get_parsed_data_from_file(large_log)
            buckets, dimensions = transform.get_heatmap_data(data, 1, 1, -1, 1)
            self.assertEqual(buckets, None)
            self.assertEqual(dimensions, None)
            self.assertEqual(fake_out.getvalue(), "Warning: All dimensions must be greater than zero.\n")
        with patch("sys.stdout", new=StringIO()) as fake_out:
            data = get_parsed_data_from_file(large_log)
            buckets, dimensions = transform.get_heatmap_data(data, 1, -1, 1, 1)
            self.assertEqual(buckets, None)
            self.assertEqual(dimensions, None)
            self.assertEqual(fake_out.getvalue(), "Warning: All dimensions must be greater than zero.\n")
        with patch("sys.stdout", new=StringIO()) as fake_out:
            data = get_parsed_data_from_file(large_log)
            buckets, dimensions = transform.get_heatmap_data(data, -1, 1, 1, 1)
            self.assertEqual(buckets, None)
            self.assertEqual(dimensions, None)
            self.assertEqual(fake_out.getvalue(), "Warning: All dimensions must be greater than zero.\n")

    def test_illegal_float_case(self):
        data = get_parsed_data_from_file(large_log)
        self.assertRaises(AssertionError, transform.get_heatmap_data, data, 0.5, 1, 0.1, 0.1, True)
        self.assertRaises(AssertionError, transform.get_heatmap_data, data, 1, 1.5, 0.1, 0.1, True)

    def test_non_empty_case(self):
        data = get_parsed_data_from_file(large_log)
        heatmap, dimensions = transform.get_heatmap_data(data, 4, 1, 201, 44, True)
        self.assertTrue(heatmap.any() and dimensions)
        self.assertTrue(len(dimensions), 4)
        heatmap, dimensions = transform.get_heatmap_data(data, 33, 33, 33, 33, True)
        self.assertTrue(heatmap.any() and dimensions)
        self.assertTrue(len(dimensions), 4)


if __name__ == "__main__":
    utest.main()
