__author__ = 'ameadows'

import unittest

from etltest.data_connector import DataConnector


class DataConnectorTests(unittest.TestCase):

    def setUp(self):

        self.source = 'etlUnitTest'
        self.table = 'users'
        self.records = [1, 2]

    def test_database_connection(self):
        print DataConnector(self.source).generate_data(self.table, self.records)

    # def test_insert_data(self):