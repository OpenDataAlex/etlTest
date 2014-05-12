"""
    This module tests the yaml_parser module.
"""

__author__ = 'ameadows'

import unittest
import yaml
import json
from etltest.utilities.yaml_parser import YAMLParser

test_dir = "/home/ameadows/PycharmProjects/etlTest/etltest/samples/test/"
data_dir = "/home/ameadows/PycharmProjects/etlTest/etltest/samples/data/"
test_file = test_dir + "dataMart/users.yml"
data_file = data_dir + "etlUnitTest/users.yml"


class yaml_parser_tests(unittest.TestCase):
    maxDiff = None

    def test_process_test_file(self):
        given_result = YAMLParser().read_file(test_file)
        expected_result = "{'testFirstNameLower': {'testSuites': {'suite': 'userDim'}," \
                          " 'desc': 'Test for process that lower cases the first name field of a users table record.'," \
                          " 'query': {'from': 'users', 'where': 'user_id = 2', 'select': 'first_name'}," \
                          " 'result': 'sarah', 'dataset': {'source': 'etlUnitTest'}}," \
                          " 'testFirstNameUpper': {'testSuites': {'suite': 'userDim'}," \
                          " 'desc': 'Test for process that upper cases the first name field of a users table record.'," \
                          " 'query': {'from': 'users', 'where': 'user_id = 2', 'select': 'first_name'}," \
                          " 'result': 'SARAH', 'dataset': {'source': 'etlUnitTest'}}," \
                          " 'testUserValidBirthday': {'testSuites': {'suite': 'userDim'}," \
                          " 'desc': 'Test for valid birth dates.'," \
                          " 'query': {'from': 'users', 'where': 'user_id IN (1, 2)', 'select': 'birthday'}," \
                          " 'result': {1: '01-01-1900', 2: '02-02-2000'}, 'dataset': {'source': 'etlUnitTest'}}}"
        self.assertEqual(json.dumps(tuple(given_result)), expected_result)

    def test_process_data_file(self):
        given_result = YAMLParser().read_file(data_file)
        expected_result = ""
        self.assertEqual(json.dumps(given_result), expected_result)