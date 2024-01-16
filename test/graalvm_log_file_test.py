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
        self.assertEqual(2.318, self.gc_event_dataframes["Time"][0])
        self.assertEqual(2.370, self.gc_event_dataframes["Time"][1])

    def test_time_unit(self):
        self.assertEqual("s", self.gc_event_dataframes["TimeUnit"][0])
        self.assertEqual("s", self.gc_event_dataframes["TimeUnit"][1])

    def test_event_name(self):
        self.assertEqual("Incremental GC", self.gc_event_dataframes["EventName"][0])
        self.assertEqual("Full GC", self.gc_event_dataframes["EventName"][1])

    def test_additional_event_info(self):
        self.assertTrue(contains(self.gc_event_dataframes["AdditionalEventInfo"], "Collect on allocation"), "'Collect on allocation' not recognized")

    def test_heap_before_gc(self):
        self.assertEqual(16.00, self.gc_event_dataframes["HeapBeforeGC"][0])
        self.assertEqual(17.00, self.gc_event_dataframes["HeapBeforeGC"][1])

    def test_heap_after_gc(self):
        self.assertEqual(4, self.gc_event_dataframes["HeapAfterGC"][0])
        self.assertEqual(4, self.gc_event_dataframes["HeapAfterGC"][1])

    def test_duration_ms(self):
        self.assertEqual(4.495, self.gc_event_dataframes["Duration_milliseconds"][0])
        self.assertEqual(11.971, self.gc_event_dataframes["Duration_milliseconds"][1])

if __name__ == "__main__":
    unittest.main()
