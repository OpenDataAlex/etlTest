#!/usr/bin/python
#
# This file was created by etlTest.
#

# These tests are also run as part of the following suites:
#
#    dataMart
#
# The following processes are executed for these tests:
#
#    PDI:
#      data_mart/user_dim_jb.kjb

import unittest
import sqlalchemy
from etltest.code_executor import CodeExecutor
from etltest.data_connector import DataConnector


class DataMartUsersDimTest(unittest.TestCase):

    def setUp(self):
        # Queries for loading test data.
          DataConnector(etlUnitTest).insert_data(users, [1, 2])

    def tearDown(self):
       # Clean up testing environment.

        DataConnector(etlUnitTest).truncate_data(users)

    def testFirstNameLower(suite):
        # Test for process that lower cases the first name field of a users table record.

        given_result = DataConnectory(etlUnitTest).select_data()

        expected_result = "sarah"

        self.assertEqual(given_result, expected_result)
    def testFirstNameUpper(suite):
        # Test for process that upper cases the first name field of a users table record.

        given_result = DataConnectory(etlUnitTest).select_data()

        expected_result = "SARAH"

        self.assertEqual(given_result, expected_result)
    def testUserValidBirthday(suite):
        # Test for valid birth dates.

        given_result = DataConnectory(etlUnitTest).select_data()

        expected_result = "[{1: '01-01-1900'}, {2: '02-02-2000'}]"

        self.assertEqual(given_result, expected_result)
