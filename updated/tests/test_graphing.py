import pandas
import unittest as utest
from io import StringIO
from unittest.mock import patch
import sys

sys.path.append("/Users/ellisbrown/Desktop/Project/updated/src/")
import graphing as graph


# Important files required for testing
empty_file = "./testdata/empty_file"
small_log = "./testdata/small_log"
large_log = "./testdata/large_log"
manual_log = "./testdata/manual_log"
