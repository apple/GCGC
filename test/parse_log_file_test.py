import unittest

import sys
sys.path.append('..')

from src.read_log_file import get_parsed_data_from_file

def contains(string_list, text):
    for s in string_list:
        if text in s:
            return True
    return False

class Test_parsing_groups(unittest.TestCase):
    
    def setUp(self):
        additional_event_info_log_file = "../datasets/additional_event_info_log_file_test.log"
        metaspace_log_file = "../datasets/metaspace_log_file_test.log"
        code_cache_log_file = "../datasets/code_cache_log_file_test.log"

        additional_event_info_dataframe = get_parsed_data_from_file(additional_event_info_log_file)
        metaspace_dataframe = get_parsed_data_from_file(metaspace_log_file)
        code_cache_dataframe = get_parsed_data_from_file(code_cache_log_file)

        self.additional_event_infos = additional_event_info_dataframe["AdditionalEventInfo"]
        self.used_metaspace_after_gc_with_unit = metaspace_dataframe["UsedMetaspaceAfterGCWithUnit"]
        self.code_cache_flushing = code_cache_dataframe["CodeCacheFlushing"]
        self.code_heap = code_cache_dataframe["CodeHeap"]
        self.code_heap_size = code_cache_dataframe["CodeHeapSize"]
        self.code_heap_used = code_cache_dataframe["CodeHeapUsed"]
        self.code_heap_max_used = code_cache_dataframe["CodeHeapMaxUsed"]

    def test_recognize_allocation_failure(self):
        self.assertTrue(contains(self.additional_event_infos, "Allocation Failure"), "'Allocation Failure' not recognized")

    def test_recognize_system_gc(self):
        self.assertTrue(contains(self.additional_event_infos, "System.gc()"), "'System.gc()' not recognized")

    def test_used_metaspace_after_gc_with_unit(self):
        self.assertEqual("3821K", self.used_metaspace_after_gc_with_unit[0])
        self.assertEqual("896M", self.used_metaspace_after_gc_with_unit[1])
        self.assertEqual("359G", self.used_metaspace_after_gc_with_unit[2])
        self.assertEqual("605K", self.used_metaspace_after_gc_with_unit[3])
        self.assertEqual("620M", self.used_metaspace_after_gc_with_unit[4])
        self.assertEqual("645G", self.used_metaspace_after_gc_with_unit[5])
        self.assertEqual("562K", self.used_metaspace_after_gc_with_unit[6])
        self.assertEqual("7605M", self.used_metaspace_after_gc_with_unit[7])
        self.assertEqual("623G", self.used_metaspace_after_gc_with_unit[8])

    def test_code_cache(self):
        self.assertEqual("non-profiled nmethods", self.code_heap[0])
        self.assertEqual(2272, self.code_heap_size[0])
        self.assertEqual(207, self.code_heap_used[0])
        self.assertEqual(207, self.code_heap_max_used[0])
        self.assertEqual("profiled nmethods", self.code_heap[1])
        self.assertEqual(2268, self.code_heap_size[1])
        self.assertEqual(1269, self.code_heap_used[1])
        self.assertEqual(1269, self.code_heap_max_used[1])
        self.assertEqual("non-nmethods", self.code_heap[2])
        self.assertEqual(5700, self.code_heap_size[2])
        self.assertEqual(1114, self.code_heap_used[2])
        self.assertEqual(1126, self.code_heap_max_used[2])
        self.assertEqual(" CodeCache flushing", self.code_cache_flushing[3])

if __name__ == "__main__":
    unittest.main()
