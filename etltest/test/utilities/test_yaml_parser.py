"""
    This module tests the yaml_parser module.
"""

__author__ = 'ameadows'

import unittest
import yaml
import json
from etltest.utilities.yaml_parser import YAMLParser

test_dir = "~/etlTest/etltest/samples/test/"
data_dir = "~/etlTest/etltest/samples/data/"
test_file = test_dir + "dataMart/users.yml"
data_file = data_dir + "etlUnitTest/users.yml"


class yaml_parser_tests(unittest.TestCase):
    maxDiff = None

    # Testing test yaml file for correct processing.
    def test_process_test_file(self):
        given_result = YAMLParser().read_file(test_file)
        expected_result = '[{"testFirstNameLower": {"testSuites": {"suite": "userDim"},' \
                          ' "dataset": {"source": "etlUnitTest"}, "desc": "Test for process that lower cases the first' \
                          ' name field of a users table record.", "result": "sarah", "query": {"where": "user_id = 2",' \
                          ' "from": "users", "select": "first_name"}}, "testUserValidBirthday": {"testSuites": ' \
                          '{"suite": "userDim"}, "dataset": {"source": "etlUnitTest"}, "desc": "Test for valid birth' \
                          ' dates.", "result": {"1": "01-01-1900", "2": "02-02-2000"}, "query": ' \
                          '{"where": "user_id IN (1, 2)", "from": "users", "select": "birthday"}},' \
                          ' "testFirstNameUpper": {"testSuites": {"suite": "userDim"}, "dataset": {"source": ' \
                          '"etlUnitTest"}, "desc": "Test for process that upper cases the first name field of a users' \
                          ' table record.", "result": "SARAH", "query": {"where": "user_id = 2",' \
                          ' "from": "users", "select": "first_name"}}}]'

        self.assertItemsEqual(json.dumps(tuple(given_result)), expected_result)

    # Testing data yaml file for correct processing.
    def test_process_data_file(self):
        given_result = YAMLParser().read_file(data_file)
        expected_result = '[{"1": {"first_name": "Bob", "last_name": "Richards", "birthday": "01-40-2000",' \
                          ' "zipcode": 55555}, "2": {"first_name": "Sarah", "last_name": "Jenkins",' \
                          ' "birthday": "02-02-2000", "zipcode": 12345}}]'
        self.assertItemsEqual(json.dumps(tuple(given_result)), expected_result)


    # Testing a directory of test yaml files to verify they are processed correctly.
    def test_process_test_dir(self):
        given_result = YAMLParser().read_dir(test_dir)
        expected_result = '[{"testFirstNameLower": {"testSuites": {"suite": "userDim"},' \
                          ' "dataset": {"source": "etlUnitTest"}, "desc": "Test for process that lower cases the first' \
                          ' name field of a users table record.", "result": "sarah", "query": {"where": "user_id = 2",' \
                          ' "from": "users", "select": "first_name"}}, "testUserValidBirthday": {"testSuites": ' \
                          '{"suite": "userDim"}, "dataset": {"source": "etlUnitTest"}, "desc": "Test for valid birth' \
                          ' dates.", "result": {"1": "01-01-1900", "2": "02-02-2000"}, "query": ' \
                          '{"where": "user_id IN (1, 2)", "from": "users", "select": "birthday"}},' \
                          ' "testFirstNameUpper": {"testSuites": {"suite": "userDim"}, "dataset": {"source": ' \
                          '"etlUnitTest"}, "desc": "Test for process that upper cases the first name field of a users' \
                          ' table record.", "result": "SARAH", "query": {"where": "user_id = 2",' \
                          ' "from": "users", "select": "first_name"}}}]'

        self.assertItemsEqual(json.dumps(tuple(given_result)), expected_result)

    # Testing a directory of data yaml files to verify they are processed correctly.
    def test_process_data_dir(self):
        given_result = YAMLParser().read_dir(data_dir)
        expected_result = '[{"1": {"first_name": "Bob", "last_name": "Richards", "birthday": "01-40-2000",' \
                          ' "zipcode": 55555}, "2": {"first_name": "Sarah", "last_name": "Jenkins",' \
                          ' "birthday": "02-02-2000", "zipcode": 12345}}]'

        self.assertItemsEqual(json.dumps(tuple(given_result)), expected_result)
