#!/usr/bin/python
#
# This file was created by etlTest.
#

# These tests are also run as part of the following suites:
#
#    LoadDataMart
#
# and are also run for the following sources/tables:
#    etlUnitTest : users

import unittest
import datetime
from os import path

from etltest.data_connector import DataConnector
from etltest.process_executor import ProcessExecutor
from etltest.utilities.settings_manager import SettingsManager


class PDILoadUsersDimTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
          # Queries for loading test data.
            DataConnector("etlUnitTest").insert_data("users", [1, 2])

            PDI_settings = SettingsManager().get_tool("PDI")
            PDI_code_path = SettingsManager().system_variable_replace(PDI_settings["code_path"])
            ProcessExecutor("PDI").execute_process("job",
            path.join(PDI_code_path, "data_mart/user_dim_jb.kjb"))

    @classmethod
    def tearDownClass(cls):
       # Clean up testing environment.

        DataConnector("etlUnitTest").truncate_data("users")

    def testFirstNameNotLower(self):
        # Ensures that the first name field is not lower case after being processed.

        given_result = DataConnector("etlUnitTest").select_data("first_name",
                        "user_dim", "user_id = 2")

        expected_result = [{'first_name': 'sarah'}]

        self.assertNotEqual(given_result, expected_result)

    def testFirstNameUpper(self):
        # Test for process that upper cases the first name field of a users table record.

        given_result = DataConnector("etlUnitTest").select_data("first_name",
                        "user_dim", "user_id = 2")

        expected_result = [{'first_name': 'SARAH'}]

        self.assertEqual(given_result, expected_result)

    def testUserValidBirthday(self):
        # Test for valid birth dates.

        given_result = DataConnector("etlUnitTest").select_data("birthday",
                        "user_dim", "user_id IN (1, 2)")

        expected_result = [{'birthday': datetime.date(2000, 1, 4)}, {'birthday': datetime.date(2000, 2, 2)}]

        self.assertEqual(given_result, expected_result)

    def testIsActiveTrue(self):
        # Passes if is_active field is set to true.

        given_result = DataConnector("etlUnitTest").select_data("is_active",
                        "users", "user_id = 2")

        self.assertTrue(given_result)

    def testIsActiveFalse(self):
        # Passes if is_active field is set to false.

        given_result = DataConnector("etlUnitTest").select_data("is_active",
                        "users", "user_id = 1")

        self.assertFalse(given_result)


if __name__ == "__main__":
    unittest.main()