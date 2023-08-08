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
        self.assertEqual(37400, self.gc_event_dataframes["Time"][0])
        self.assertEqual(37427, self.gc_event_dataframes["Time"][1])

    def test_time_unit(self):
        self.assertEqual("msec", self.gc_event_dataframes["TimeUnit"][0])
        self.assertEqual("msec", self.gc_event_dataframes["TimeUnit"][1])

    def test_event_name(self):
        self.assertEqual("Full GC", self.gc_event_dataframes["EventName"][0])
        self.assertEqual("Incremental GC", self.gc_event_dataframes["EventName"][1])

    def test_additional_event_info(self):
        self.assertTrue(contains(self.gc_event_dataframes["AdditionalEventInfo"], "CollectOnAllocation"), "'CollectOnAllocation' not recognized")

    def test_heap_before_gc(self):
        self.assertEqual(26624, self.gc_event_dataframes["HeapBeforeGC_kb"][0])
        self.assertEqual(31744, self.gc_event_dataframes["HeapBeforeGC_kb"][1])

    def test_heap_after_gc(self):
        self.assertEqual(5120, self.gc_event_dataframes["HeapAfterGC_kb"][0])
        self.assertEqual(7168, self.gc_event_dataframes["HeapAfterGC_kb"][1])

    def test_duration_ms(self):
        self.assertEqual(0.0067170, self.gc_event_dataframes["Duration_seconds"][0])
        self.assertEqual(0.0029815, self.gc_event_dataframes["Duration_seconds"][1])

if __name__ == "__main__":
    unittest.main()
