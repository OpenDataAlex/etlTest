__author__ = 'ameadows'

import unittest
import datetime

from etltest.data_connector import DataConnector
from etltest.utilities.settings_manager import SettingsManager

class DataConnectorTests(unittest.TestCase):

    def setUp(self):

        SettingsManager().first_run_test()

        self.source = 'etlUnitTest'
        self.table = 'users'

    def test_bad_connection(self):
        #Testing to see if a non existant connection will fail gracefully.
        records = [1, 2]

        with self.assertRaises(KeyError) as raises:
            DataConnector("BadConnection").generate_data(self.table, records)

        self.assertEqual(raises.exception.message, "BadConnection")

    def test_generate_data_subset(self):
        #Testing to see if a subset of data is generated and not the full data set.
        records = [1, 2]
        given_result = DataConnector(self.source).generate_data(self.table, records)
        expected_result = [{'first_name': 'Bob', 'last_name': 'Richards', 'user_id': 1, 'zipcode': 55555,
                            'birthday': datetime.date(2000, 1, 4)}, {'first_name': 'Sarah', 'last_name': 'Jenkins', 'user_id': 2,
                                                        'zipcode': 12345, 'birthday': datetime.date(2000, 2, 2)}]

        self.assertEqual(given_result, expected_result)

    def test_generate_data_subset_non_existent_records(self):
        # Testing to see if a record doesn't exist, the data generator will only return valid records.
        records = [1, 2, 20]
        given_result = DataConnector(self.source).generate_data(self.table, records)
        expected_result = [{'first_name': 'Bob', 'last_name': 'Richards', 'user_id': 1, 'zipcode': 55555,
                            'birthday': datetime.date(2000, 1, 4)}, {'first_name': 'Sarah', 'last_name': 'Jenkins', 'user_id': 2,
                                                        'zipcode': 12345, 'birthday': datetime.date(2000, 2, 2)}]

        self.assertEqual(given_result, expected_result)

    def test_insert_data(self):
        # Testing to see if the data set will be inserted correctly.
        records = [1, 2]
        DataConnector(self.source).insert_data(self.table, records)
        given_result = DataConnector(self.source).select_data("all_columns", self.table, "user_id = 1")
        expected_result = {'first_name': 'Bob', 'last_name': 'Richards', 'user_id': 1, 'zipcode': '55555'
                            , 'birthday': datetime.date(2000, 1, 4)}, {'first_name': 'Sarah', 'last_name': 'Jenkins'
                            , 'user_id': 2, 'zipcode': '12345', 'birthday': datetime.date(2000, 2, 2)}

        self.assertItemsEqual(given_result, expected_result)

    def test_truncate_data(self):
        # Testing to see if the data set will be removed completely.
        DataConnector(self.source).truncate_data(self.table)
        given_result = DataConnector(self.source).select_data(self.table)
        expected_result = []

        self.assertEqual(given_result, expected_result)

    def test_select_all_data(self):
        # Testing to see if the full data set will be selected correctly.
        given_result = DataConnector(self.source).select_data("all_columns", self.table, "user_id = 1")
        expected_result = [{'first_name': 'Bob', 'last_name': 'Richards', 'user_id': 1, 'zipcode': '55555'
                            , 'birthday': datetime.date(2000, 1, 4)}, {'first_name': 'Sarah', 'last_name': 'Jenkins'
                            , 'user_id': 2, 'zipcode': '12345', 'birthday': datetime.date(2000, 2, 2)}]

        self.assertEqual(given_result, expected_result)

    def test_select_single_column_data(self):
        # Testing to see if the data set will be selected correctly.
        DataConnector(self.source).insert_data(self.table, records)
        given_result = DataConnector(self.source).select_data("[first_name, last_name]", self.table, "user_id = 1")
        expected_result = [{'first_name': 'Bob', 'last_name': 'Richards'}]

        self.assertEqual(given_result, expected_result)
