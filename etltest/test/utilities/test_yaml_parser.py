"""
    This module tests the yaml_parser module.
"""

__author__ = 'ameadows'

import unittest

from etltest.utilities.yaml_parser import YAMLParser
from etltest.utilities.settings_manager import SettingsManager


tmp_path = SettingsManager().get_file_location()
test_dir = tmp_path + "/etltest/samples/test/"
data_dir = tmp_path + "/etltest/samples/data/"
test_file = test_dir + "dataMart/users_dim.yml"
data_file = data_dir + "etlUnitTest/users_dim.yml"


class YamlParserTests(unittest.TestCase):
    maxDiff = None

    # Testing test yaml file for correct processing.
    def test_process_test_file(self):
        given_result = YAMLParser().read_file(test_file)
        expected_result = [{'DataMart\\Users': [{'suites': [{'suite': 'dataMart'}, {'suite': 'userDim'}]
                          , 'desc': 'Test for process that lower cases the first name field of a users table record.'
                          , 'query': [{'from': 'users', 'where': 'user_id = 2', 'result': 'sarah'
                          , 'select': 'first_name'}], 'name': 'testFirstNameLower', 'dataset': [{'source': 'etlUnitTest'
                          , 'table': 'users', 'records': [2]}]}, {'suites': [{'suite': 'dataMart'}
                          , {'suite': 'userDim'}]
                          , 'desc': 'Test for process that upper cases the first name field of a users table record.'
                          , 'query': [{'from': 'users', 'where': 'user_id = 2', 'result': 'SARAH'
                          , 'select': 'first_name'}], 'name': 'testFirstNameUpper', 'dataset': [{'source': 'etlUnitTest'
                          , 'table': 'users', 'records': [2]}]}, {'suites': [{'suite': 'userDim'}]
                          , 'desc': 'Test for valid birth dates.', 'query': [{'from': 'users'
                          , 'where': 'user_id IN (1, 2)', 'result': [{1: '01-01-1900'}, {2: '02-02-2000'}]
                          , 'select': 'birthday'}], 'name': 'testUserValidBirthday'
                          , 'dataset': [{'source': 'etlUnitTest', 'table': 'users', 'records': [1, 2]}]}]}]

        self.assertItemsEqual(given_result, expected_result)

    # Testing data yaml file for correct processing.
    def test_process_data_file(self):
        given_result = YAMLParser().read_file(data_file)
        expected_result = [{1: {"first_name": "Bob", "last_name": "Richards", "birthday": "01-40-2000",
                           "zipcode": 55555}, 2: {"first_name": "Sarah", "last_name": "Jenkins",
                           "birthday": "02-02-2000", "zipcode": 12345}}]
        self.assertItemsEqual(given_result, expected_result)


    # Testing a directory of test yaml files to verify they are processed correctly.
    def test_process_test_dir(self):
        given_result = YAMLParser().read_dir(test_dir)
        expected_result = [{'DataMart\\Users': [{'suites': [{'suite': 'dataMart'}, {'suite': 'userDim'}]
                        , 'desc': 'Test for process that lower cases the first name field of a users table record.'
                        , 'query': [{'from': 'users', 'where': 'user_id = 2', 'result': 'sarah'
                        , 'select': 'first_name'}], 'name': 'testFirstNameLower', 'dataset': [{'source': 'etlUnitTest'
                        , 'table': 'users', 'records': [2]}]}, {'suites': [{'suite': 'dataMart'}, {'suite': 'userDim'}]
                        , 'desc': 'Test for process that upper cases the first name field of a users table record.'
                        , 'query': [{'from': 'users', 'where': 'user_id = 2', 'result': 'SARAH'
                        , 'select': 'first_name'}], 'name': 'testFirstNameUpper', 'dataset': [{'source': 'etlUnitTest'
                        , 'table': 'users', 'records': [2]}]}, {'suites': [{'suite': 'userDim'}]
                        , 'desc': 'Test for valid birth dates.', 'query': [{'from': 'users'
                        , 'where': 'user_id IN (1, 2)', 'result': [{1: '01-01-1900'}, {2: '02-02-2000'}]
                        , 'select': 'birthday'}], 'name': 'testUserValidBirthday', 'dataset': [{'source': 'etlUnitTest'
                        , 'table': 'users', 'records': [1, 2]}]}]}]

        self.assertEqual(given_result, expected_result)

    # Testing a directory of data yaml files to verify they are processed correctly.
    def test_process_data_dir(self):
        given_result = YAMLParser().read_dir(data_dir)
        expected_result = [{1: {"first_name": "Bob", "last_name": "Richards", "birthday": "01-40-2000",
                           "zipcode": 55555}, 2: {"first_name": "Sarah", "last_name": "Jenkins",
                           "birthday": "02-02-2000", "zipcode": 12345}}]

        self.assertEqual(given_result, expected_result)
