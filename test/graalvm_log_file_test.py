import unittest

import sys
sys.path.append('..')

from src.read_log_file import get_parsed_data_from_file

def contains(string_list, text):
    for s in string_list:
        if text in s:
            return True
    return False

class Test_parsing_graalvm_log_file(unittest.TestCase):

    def setUp(self):
        log_file = "../datasets/graalvm_log_file_test.log"
        # log_file = "../datasets/parse_log_file_test.log"
        self.gc_event_dataframes = get_parsed_data_from_file(log_file)

    def test_time(self):
        self.assertEqual(658.653, self.gc_event_dataframes["Time"][0])
        self.assertEqual(658.793, self.gc_event_dataframes["Time"][1])

    def test_time_unit(self):
        self.assertEqual("s", self.gc_event_dataframes["TimeUnit"][0])
        self.assertEqual("s", self.gc_event_dataframes["TimeUnit"][1])

    def test_event_name(self):
        self.assertEqual("Incremental GC", self.gc_event_dataframes["EventType"][0])
        self.assertEqual("Full GC", self.gc_event_dataframes["EventType"][1])

    def test_additional_event_info(self):
        self.assertTrue(contains(self.gc_event_dataframes["AdditionalEventInfo"], "Collect on allocation"), "'Collect on allocation' not recognized")

    def test_heap_before_gc(self):
        self.assertEqual(54.50, self.gc_event_dataframes["HeapBeforeGC"][0])
        self.assertEqual(53.50, self.gc_event_dataframes["HeapBeforeGC"][1])

    def test_heap_after_gc(self):
        self.assertEqual(9.50, self.gc_event_dataframes["HeapAfterGC"][0])
        self.assertEqual(9, self.gc_event_dataframes["HeapAfterGC"][1])

    def test_duration_ms(self):
        self.assertEqual(3.346, self.gc_event_dataframes["Duration_milliseconds"][0])
        self.assertEqual(23.244, self.gc_event_dataframes["Duration_milliseconds"][1])

if __name__ == "__main__":
    unittest.main()
