__author__ = 'ameadows'

import unittest

from etltest.data_connector import DataConnector


class DataConnectorTests(unittest.TestCase):

    def setUp(self):

        self.source = 'etlUnitTest'
        self.table = 'users'
        self.records = [1, 2]

    def test_password_encryption(self):
        given_result = DataConnector(self.source).encrypt_password('password', 'salt')
        expected_result = "$5$rounds=110000$zmwWGEzQuB0Wlvr7$8jDVBArZwGApZBRZIonurt3RKmRlnDRvmE1l8uOp1P6"

        self.assertEqual(given_result, expected_result)

    # def test_database_connection(self):
    #     print DataConnector(self.source).generate_data(self.table, self.records)

    # def test_insert_data(self):