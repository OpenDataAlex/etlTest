"""
    This module tests the yaml_parser module.
"""

__author__ = 'ameadows'

import unittest
import datetime
import os

from etltest.utilities.yaml_parser import YAMLParser
from etltest.utilities.settings_manager import SettingsManager


class YamlParserTests(unittest.TestCase):
    """
    The main class for the the YamlParser test suite.
    """
    def setUp(self):
        SettingsManager().first_run_test()
        self.tmp_path = SettingsManager().get_file_location()
        self.data_loc = SettingsManager().find_setting('Locations', 'data')
        self.test_dir = self.tmp_path + "/etltest/samples/test/"
        self.data_dir = self.tmp_path + "/etltest/samples/data/"
        self.test_file = self.test_dir + "dataMart/users_dim.yml"
        self.data_file = self.data_dir + "etlUnitTest/users.yml"
        self.maxDiff = None

    def test_process_test_file_whitespace(self):
        """
        Testing that whitespace will not impact the reading of files.
        """
        self.test_file = " " + self.test_file
        given_result = YAMLParser().read_file(self.test_file)
        expected_result = [{'DataMart\\UsersDim': {'suites': [{'suite': 'dataMart'}], 'processes': [
            {'tool': 'PDI', 'processes': [{'type': 'job', 'name': 'data_mart/user_dim_jb.kjb'}]}], 'tests':
            [{'query': {'from': 'user_dim', 'where': 'user_id = 2', 'result': {'first_name': 'sarah'}, 'select':
                'first_name', 'source': 'etlUnitTest'}, 'type': 'NotEqual', 'name': 'testFirstNameNotLower',
              'desc': 'Ensures that the first name field is not lower case after being processed.'},
             {'query': {'from': 'user_dim', 'where': 'user_id = 2', 'result': {'first_name': 'SARAH'},
                        'select': 'first_name', 'source': 'etlUnitTest'}, 'type': 'Equal', 'name': 'testFirstNameUpper',
              'desc': 'Test for process that upper cases the first name field of a users table record.'},
             {'query': {'from': 'user_dim', 'where': 'user_id IN (1, 2)',
                        'result': "{'birthday': datetime.date(2000, 1, 4)}, {'birthday': datetime.date(2000, 2, 2)}",
                        'select': 'birthday', 'source': 'etlUnitTest'},
              'name': 'testUserValidBirthday', 'desc': 'Test for valid birth dates.'},
             {'query': {'from': 'users', 'where': 'user_id = 2', 'select': 'is_active', 'source': 'etlUnitTest'},
              'type': 'BooleanTrue', 'name': 'testIsActiveTrue', 'desc': 'Passes if is_active field is set to true.'},
             {'query': {'from': 'users', 'where': 'user_id = 1', 'select': 'is_active', 'source': 'etlUnitTest'},
              'type': 'BooleanFalse', 'name': 'testIsActiveFalse', 'desc': 'Passes if is_active field is set to false.'}
            ], 'dataset': [{'source': 'etlUnitTest', 'table': 'users', 'records': [1, 2]}]}}]

        self.assertCountEqual(given_result, expected_result)

    def test_process_test_file(self):
        """
        Testing test yaml file to ensure correct processing.
        """
        given_result = YAMLParser().read_file(self.test_file)
        expected_result = [{'DataMart\\UsersDim': {'suites': [{'suite': 'dataMart'}], 'processes':
            [{'tool': 'PDI', 'processes': [{'type': 'job', 'name': 'data_mart/user_dim_jb.kjb'}]}], 'tests':
            [{'query': {'from': 'user_dim', 'where': 'user_id = 2', 'result': {'first_name': 'sarah'},
                        'select': 'first_name', 'source': 'etlUnitTest'}, 'type': 'NotEqual',
              'name': 'testFirstNameNotLower',
              'desc': 'Ensures that the first name field is not lower case after being processed.'},
             {'query': {'from': 'user_dim', 'where': 'user_id = 2', 'result': {'first_name': 'SARAH'},
                        'select': 'first_name', 'source': 'etlUnitTest'}, 'type': 'Equal',
              'name': 'testFirstNameUpper',
              'desc': 'Test for process that upper cases the first name field of a users table record.'},
             {'query': {'from': 'user_dim', 'where': 'user_id IN (1, 2)',
                        'result': "{'birthday': datetime.date(2000, 1, 4)}, {'birthday': datetime.date(2000, 2, 2)}",
                        'select': 'birthday', 'source': 'etlUnitTest'}, 'name': 'testUserValidBirthday',
              'desc': 'Test for valid birth dates.'}, {'query': {'from': 'users', 'where': 'user_id = 2',
                                                                 'select': 'is_active', 'source': 'etlUnitTest'},
                                                       'type': 'BooleanTrue', 'name': 'testIsActiveTrue',
                                                       'desc': 'Passes if is_active field is set to true.'},
             {'query': {'from': 'users', 'where': 'user_id = 1', 'select': 'is_active', 'source': 'etlUnitTest'},
              'type': 'BooleanFalse', 'name': 'testIsActiveFalse', 'desc': 'Passes if is_active field is set to false.'}
            ], 'dataset': [{'source': 'etlUnitTest', 'table': 'users', 'records': [1, 2]}]}}]

        self.assertCountEqual(given_result, expected_result)

    def test_process_data_file(self):
        """
        Testing the data yaml sample file to ensure correct processing.
        """
        given_result = YAMLParser().read_file(self.data_file)
        expected_result = [{1: {'first_name': 'Bob', 'last_name': 'Richards', 'user_id': 1, 'zipcode': 55555,
                                'birthday': datetime.date(2000, 1, 4), 'is_active': 0}, 2:
            {'first_name': 'Sarah', 'last_name': 'Jenkins', 'user_id': 2, 'zipcode': 12345,
             'birthday': datetime.date(2000, 2, 2), 'is_active': 1},
                            3: {'first_name': 'Frank', 'last_name': 'Williams', 'user_id': 3, 'zipcode': 56789,
                                'birthday': datetime.date(1972, 3, 3), 'is_active': 0},
                            4: {'first_name': 'Thomas', 'last_name': 'Stedding', 'user_id': 4, 'zipcode': 44444,
                                'birthday': datetime.date(1923, 1, 4), 'is_active': 1}}]
        self.assertCountEqual(given_result, expected_result)

    def test_process_test_dir(self):
        """
        Testing a directory of test yaml files to verify they are processed correctly.
        """
        given_result = YAMLParser().read_dir(os.path.join(self.test_dir, 'dataMart'))
        expected_result = [{'DataMart\\UsersFact': {'tests': [{'query': {'from': 'user_dim', 'where': 'user_id = 2',
                            'select': 'first_name', 'result': {'first_name': 'sarah'}, 'source': 'etlUnitTest'},
                            'name': 'testFirstNameNotLower', 'type': 'NotEqual',
                            'desc': 'Ensures that the first name field is not lower case after being processed.'}, {'query': {'from': 'user_dim', 'where': 'user_id = 2', 'select': 'first_name', 'result': {'first_name': 'SARAH'}, 'source': 'etlUnitTest'}, 'name': 'testFirstNameUpper', 'type': 'Equal', 'desc': 'Test for process that upper cases the first name field of a users table record.'}, {'query': {'from': 'user_dim', 'where': 'user_id IN (1, 2)', 'select': 'birthday', 'result': "{'birthday': datetime.date(2000, 1, 4)}, {'birthday': datetime.date(2000, 2, 2)}", 'source': 'etlUnitTest'}, 'name': 'testUserValidBirthday', 'desc': 'Test for valid birth dates.'}, {'query': {'from': 'users', 'where': 'user_id = 2', 'select': 'is_active', 'source': 'etlUnitTest'}, 'name': 'testIsActiveTrue', 'type': 'BooleanTrue', 'desc': 'Passes if is_active field is set to true.'}, {'query': {'from': 'users', 'where': 'user_id = 1', 'select': 'is_active', 'source': 'etlUnitTest'}, 'name': 'testIsActiveFalse', 'type': 'BooleanFalse', 'desc': 'Passes if is_active field is set to false.'}], 'processes': [{'tool': 'PDI', 'processes': [{'name': 'data_mart/user_fact_jb.kjb', 'type': 'job'}]}], 'dataset': [{'records': [1, 2], 'table': 'users', 'source': 'etlUnitTest'}], 'suites': [{'suite': 'dataMart'}]}},{'DataMart\\UsersDim': {'processes': [{'processes': [{'name': 'data_mart/user_dim_jb.kjb',
                                                                                 'type': 'job'}], 'tool': 'PDI'}],
                                                   'dataset': [{'source': 'etlUnitTest', 'table': 'users',
                                                                'records': [1, 2]}], 'tests':
            [{'name': 'testFirstNameNotLower', 'query': {'source': 'etlUnitTest', 'where': 'user_id = 2',
                                                         'from': 'user_dim', 'result': {'first_name': 'sarah'},
                                                         'select': 'first_name'}, 'type': 'NotEqual',
              'desc': 'Ensures that the first name field is not lower case after being processed.'},
             {'name': 'testFirstNameUpper', 'query': {'source': 'etlUnitTest', 'where': 'user_id = 2',
                                                      'from': 'user_dim', 'result': {'first_name': 'SARAH'},
                                                      'select': 'first_name'}, 'type': 'Equal',
              'desc': 'Test for process that upper cases the first name field of a users table record.'},
             {'name': 'testUserValidBirthday', 'query': {'source': 'etlUnitTest', 'where': 'user_id IN (1, 2)',
                                                         'from': 'user_dim',
                                                         'result': "{'birthday': datetime.date(2000, 1, 4)}, "
                                                                   "{'birthday': datetime.date(2000, 2, 2)}",
                                                         'select': 'birthday'}, 'desc': 'Test for valid birth dates.'},
             {'name': 'testIsActiveTrue', 'query': {'source': 'etlUnitTest', 'where': 'user_id = 2', 'from': 'users',
                                                    'select': 'is_active'}, 'type': 'BooleanTrue',
              'desc': 'Passes if is_active field is set to true.'}, {'name': 'testIsActiveFalse', 'query':
                {'source': 'etlUnitTest', 'where': 'user_id = 1', 'from': 'users', 'select': 'is_active'},
                                                                    'type': 'BooleanFalse',
                                                                    'desc': 'Passes if is_active field is set to false.'
                                                                             ''}], 'suites': [{'suite': 'dataMart'}]}}]

        self.assertCountEqual(given_result, expected_result)

    def test_process_data_dir(self):
        """
        Testing a directory of data yaml files to verify they are processed correctly.
        """
        given_result = YAMLParser().read_dir(self.data_dir)
        expected_result = [{1: {'city': 'Young America', 'state': 'Minnesota', 'user_geo_ref_id': 1, 'zipcode': 55555,
                                'country': 'United States'},
                            2: {'city': 'Schenectady', 'state': 'New York', 'user_geo_ref_id': 2, 'zipcode': 12345,
                                'country': 'United States'},
                            3: {'city': 'Colton', 'state': 'California', 'user_geo_ref_id': 3, 'zipcode': 56789,
                                'country': 'United States'},
                            4: {'city': 'Newton Falls', 'state': 'Ohio', 'user_geo_ref_id': 4, 'zipcode': 44444,
                                'country': 'United States'}},
                           {'Young America': {'city': 'Young America', 'state': 'Minnesota', 'user_geo_ref_id': 1,
                                              'zipcode': 55555, 'country': 'United States'},
                            'Colton': {'city': 'Colton', 'state': 'California', 'user_geo_ref_id': 3, 'zipcode': 56789,
                                       'country': 'United States'},
                            'Schenectady': {'city': 'Schenectady', 'state': 'New York', 'user_geo_ref_id': 2,
                                            'zipcode': 12345, 'country': 'United States'},
                            'Newton Falls': {'city': 'Newton Falls', 'state': 'Ohio', 'user_geo_ref_id': 4,
                                             'zipcode': 44444, 'country': 'United States'}},
                           {1: {'first_name': 'Bob', 'last_name': 'Richards', 'user_id': 1, 'zipcode': 55555,
                                'birthday': datetime.date(2000, 1, 4), 'is_active': 0},
                            2: {'first_name': 'Sarah', 'last_name': 'Jenkins', 'user_id': 2, 'zipcode': 12345,
                                'birthday': datetime.date(2000, 2, 2), 'is_active': 1},
                            3: {'first_name': 'Frank', 'last_name': 'Williams', 'user_id': 3, 'zipcode': 56789,
                                'birthday': datetime.date(1972, 3, 3), 'is_active': 0},
                            4: {'first_name': 'Thomas', 'last_name': 'Stedding', 'user_id': 4, 'zipcode': 44444,
                                'birthday': datetime.date(1923, 1, 4), 'is_active': 1}}]

        self.assertCountEqual(given_result, expected_result)

    def test_process_write_file_defined_column(self):
        """
        Testing that if a given column is provided, it will be used as the identifier for the records in the data file.
        """
        data_set = [{'city': 'Young America', 'state': 'Minnesota', 'user_geo_ref_id': 1, 'zipcode': 55555,
                     'country': 'United States'}, {'city': 'Colton', 'state': 'California', 'user_geo_ref_id': 3,
                                                   'zipcode': 56789, 'country': 'United States'},
                    {'city': 'Schenectady', 'state': 'New York', 'user_geo_ref_id': 2, 'zipcode': 12345,
                     'country': 'United States'}, {'city': 'Newton Falls', 'state': 'Ohio', 'user_geo_ref_id': 4,
                                                   'zipcode': 44444, 'country': 'United States'}]
        YAMLParser().write_file(data_set, 'etlUnitTest', 'user_geo_ref', 'city')

        sample_file = os.path.join(self.data_dir, 'etlUnitTest/user_geo_ref_defined_column.yml')
        output_file = os.path.join(self.data_loc, 'etlUnitTest/user_geo_ref.yml')

        with open(sample_file) as f:
            expected_result = f.read()

        with open(output_file) as f:
            given_result = f.read()

        self.assertCountEqual(given_result, expected_result)
