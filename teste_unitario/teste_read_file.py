import unittest
from unittest.mock import MagicMock
from pyspark.sql import DataFrame

from read_file import read_file


class AllTests(unittest.TestCase):

    def test_read_file(self):
        path = 'file.csv'
        result = read_file(path, MagicMock())
        assert result is not None
        assert type(result) == DataFrame