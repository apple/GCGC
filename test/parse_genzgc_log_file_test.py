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
        log_file = "../datasets/GenZGC.log"
        self.dataframe = get_parsed_data_from_file(log_file)

    def test_event_name(self):
        self.assertEqual(51543, self.dataframe.size)
        self.assertEqual("Mark Start", self.dataframe["EventName"][0])
        self.assertEqual("Major Collection", self.dataframe["EventType"][739])
        self.assertEqual(3, self.dataframe["HeapPercentFull"][773])
        self.assertEqual(" Y:", self.dataframe["Generation"][1658])
        self.assertEqual(320, self.dataframe["HeapAfterGC"][1856])

if __name__ == "__main__":
    unittest.main()
