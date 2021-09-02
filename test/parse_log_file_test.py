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
        log_file = "../datasets/parse_log_file_test.log"
        gc_event_dataframes = get_parsed_data_from_file(log_file);
        self.additional_event_infos = gc_event_dataframes["AdditionalEventInfo"] 

    def test_recognize_allocation_failure(self):
        self.assertTrue(contains(self.additional_event_infos, "Allocation Failure"), "'Allocation Failure' not recognized")

    def test_recognize_system_gc(self):
        self.assertTrue(contains(self.additional_event_infos, "System.gc()"), "'System.gc()' not recognized")

if __name__ == "__main__":
    unittest.main()
