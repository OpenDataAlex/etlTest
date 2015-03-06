"""
Testing the DataConnector module.
"""

__author__ = 'ameadows'

import unittest
import datetime

from etltest.data_connector import DataConnector
from etltest.utilities.settings_manager import SettingsManager


class DataConnectorTests(unittest.TestCase):
    """
    We first make sure that the environment is set up by using the first_run_test method.  We then set some parameters
    up to properly test for a given source and table.
    """
    def setUp(self):

        SettingsManager().first_run_test()

        self.source = 'etlUnitTest'
        self.table = 'users'
        self.records = [1, 2]

    def tearDown(self):
        DataConnector(self.source).truncate_data(self.table)

    def test_bad_connection(self):
        """
        Testing to see if a non existent connection will fail gracefully.
        """
        records = [1, 2]

        self.assertRaises(KeyError, lambda: DataConnector("BadConnection").generate_data(self.table, records))

    def test_generate_data_all(self):
        """
        Testing to see if the full data set is generated.
        """
        given_result = DataConnector(self.source).generate_data(self.table)
        expected_result = [{'first_name': 'Bob', 'last_name': 'Richards', 'user_id': 1, 'zipcode': 55555,
                            'birthday': datetime.date(2000, 1, 4), 'is_active': 0},
                           {'first_name': 'Sarah', 'last_name': 'Jenkins', 'user_id': 2, 'zipcode': 12345,
                            'birthday': datetime.date(2000, 2, 2), 'is_active': 1},
                           {'first_name': 'Frank', 'last_name': 'Williams', 'user_id': 3, 'is_active': 0,
                            'zipcode': 56789, 'birthday': datetime.date(1972, 3, 3)},
                           {'first_name': 'Thomas', 'last_name': 'Stedding',
                            'user_id': 4, 'is_active': 1, 'zipcode': 44444, 'birthday': datetime.date(1923, 1, 4)}]

        self.assertCountEqual(given_result, expected_result)

    def test_generate_data_subset(self):
        """
        Testing to see if a subset of data is generated and not the full data set.
        """
        given_result = DataConnector(self.source).generate_data(self.table, self.records)
        expected_result = [{'first_name': 'Bob', 'last_name': 'Richards', 'user_id': 1, 'zipcode': 55555,
                            'birthday': datetime.date(2000, 1, 4), 'is_active': 0},
                           {'first_name': 'Sarah', 'last_name': 'Jenkins', 'user_id': 2, 'zipcode': 12345,
                            'birthday': datetime.date(2000, 2, 2), 'is_active': 1}]

        self.assertEqual(given_result, expected_result)

    def test_generate_data_subset_non_existent_records(self):
        """
        Testing to see if a record doesn't exist, the data generator will only return valid records.
        """
        records = [1, 2, 20]
        given_result = DataConnector(self.source).generate_data(self.table, records)
        expected_result = [{'first_name': 'Bob', 'last_name': 'Richards', 'user_id': 1, 'zipcode': 55555,
                            'birthday': datetime.date(2000, 1, 4), 'is_active': 0}, {'first_name': 'Sarah'
                            , 'last_name': 'Jenkins', 'user_id': 2, 'zipcode': 12345,
                            'birthday': datetime.date(2000, 2, 2), 'is_active': 1}]

        self.assertEqual(given_result, expected_result)

    def test_insert_data(self):
        """
        Testing to see if the data set will be inserted correctly.
        """
        DataConnector(self.source).insert_data(self.table, self.records)
        given_result = DataConnector(self.source).select_data("all_columns", self.table, "user_id IN (1, 2)")
        expected_result = {'first_name': 'Bob', 'last_name': 'Richards', 'user_id': 1, 'zipcode': '55555'
                            , 'birthday': datetime.date(2000, 1, 4), 'is_active': 0}, {'first_name': 'Sarah', 'last_name': 'Jenkins'
                            , 'user_id': 2, 'zipcode': '12345', 'birthday': datetime.date(2000, 2, 2), 'is_active': 1}

        self.assertCountEqual(given_result, expected_result)

    def test_truncate_data(self):
        """
        Testing to see if the data set will be removed completely.
        """
        DataConnector(self.source).insert_data(self.table, self.records)
        DataConnector(self.source).truncate_data(self.table)
        given_result = DataConnector(self.source).select_data("all_columns", self.table)
        expected_result = []

        self.assertEqual(given_result, expected_result)

    def test_select_all_data(self):
        """
        Testing to see if the full data set will be selected correctly.
        """
        records = [1, 2]
        DataConnector(self.source).insert_data(self.table, records)
        given_result = DataConnector(self.source).select_data("all_columns", self.table, "user_id = 2")
        expected_result = [{'first_name': 'Sarah', 'last_name': 'Jenkins', 'user_id': 2, 'zipcode': '12345', 'birthday': datetime.date(2000, 2, 2), 'is_active': 1}]

        self.assertEqual(given_result, expected_result)

    def test_select_all_data_no_columns(self):
        """
        Testing that when all columns are selected, None value is passed.
        """
        given_result = DataConnector(self.source).get_table(self.table, select_stmt="all_columns")
        expected_result = DataConnector(self.source).get_table(self.table)

        self.assertCountEqual(given_result.columns._data, expected_result.columns._data)

    def test_select_multiple_column_data(self):
        """
        Testing to see if the data set will be selected correctly.
        """
        DataConnector(self.source).insert_data(self.table, self.records)
        given_result = DataConnector(self.source).select_data("first_name, last_name", self.table, "user_id = 1")
        expected_result = [{'first_name': 'Bob', 'last_name': 'Richards'}]

        self.assertEqual(given_result, expected_result)

    def test_select_single_column_data(self):
        """
        Testing to see if the data set will be selected correctly.
        """
        DataConnector(self.source).insert_data(self.table, self.records)
        given_result = DataConnector(self.source).select_data("first_name", self.table, "user_id = 1")
        expected_result = [{'first_name': 'Bob'}]

        self.assertEqual(given_result, expected_result)

    def test_select_null_column_data(self):
        """
        Testing to see if the data set that has a null in it will be selected correctly.
        """
        records = [1, 4]
        DataConnector(self.source).insert_data(self.table, records)
        given_result = DataConnector(self.source).select_data("first_name", self.table, "user_id IN (1, 4)")
        expected_result = [{'first_name': 'Bob'}, {'first_name': 'Thomas'}]

        self.assertCountEqual(given_result, expected_result)

    def test_empty_data_file(self):
        """
        Testing to ensure that if a data file being used is empty, it will throw an error.
        """
        records = [1, 4]

        with self.assertRaises(Exception) as cm:
            DataConnector(self.source).insert_data('empty_data_file', records)
        self.assertRaises(Exception, cm.exception)
