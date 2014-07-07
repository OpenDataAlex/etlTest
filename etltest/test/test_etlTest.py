__author__ = 'ameadows'

import unittest
import scripttest

from etltest.utilities.settings_manager import SettingsManager

class etlTestTests(unittest.TestCase):

    # def setUp(self):
    #     self.env = scripttest.TestFileEnvironment('./test-output')
    #     self.process = "../../etlTest.py"
    #
    #     self.in_file = SettingsManager().system_variable_replace("${"
    #                                                              "ETL_TEST_ROOT}/etltest/samples/test/dataMart/users_dim.yml")
    #     self.in_dir = SettingsManager().system_variable_replace("${ETL_TEST_ROOT}/etltest/samples/test/dataMart/")
    #
    # def test_with_empty_args(self):
    #     process = str(self.env.run("python", self.process, "-h"))
    #     given_result = process["stdout"]
    #     expected_result = ""
    #
    #     self.assertEqual(given_result, expected_result)
    #
    # def test_in_file_generation(self):
    #     file_param = u"-f '{0:s}'".format(self.in_file)
    #     process = str(self.env.run("python", self.process, file_param, "-g"))
    #     given_result = process["stdout"]
    #     expected_result = ""
    #
    #     self.assertEqual(given_result, expected_result)