"""
Testing the SettingsManager module.
"""

__author__ = 'ameadows'

import unittest
from collections import OrderedDict
import inspect
import re
import os

import appdirs

from etltest.utilities.settings import etltest_config
from etltest.utilities.settings_manager import SettingsManager


class SettingsManagerTests(unittest.TestCase):
    """
    Module for testing SettingsManager.
    """
    def setUp(self):
        """
            Setting up tests by running the first run setup and setting specific variables
            based on the config file.
        """

        SettingsManager().first_run_test()
        self.app_name = etltest_config['app_name']
        self.app_author = etltest_config['app_author']
        self.data_dir = appdirs.user_data_dir(self.app_name, self.app_author)
        self.log_dir = appdirs.user_log_dir(self.app_name, self.app_author)
        self.settings_file = os.path.join(self.data_dir, etltest_config['settings_file'])
        self.connection_file = os.path.join(self.data_dir, etltest_config['connection_file'])
        self.data_location = SettingsManager().find_setting('Locations', 'data')
        self.tools_file = os.path.join(self.data_dir, etltest_config['tools_file'])
        self.copy_file = os.path.join(self.data_dir, 'copy.test')
        self.tests_location = SettingsManager().find_setting('Locations', 'tests')
        self.output_location = SettingsManager().find_setting('Locations', 'output')

        self.maxDiff = None

    def test_data_dir_exists(self):
        """
        Testing to see if the data directory exists after the first run setup.
        """
        assert os.path.exists(self.data_dir)

    def test_log_dir_exists(self):
        """
        Testing to see if the log directory exists after the first run setup.
        """
        assert os.path.exists(self.log_dir)

    def test_settings_file_exists(self):
        """
        Testing to see if the settings file exists after the first run setup.
        """
        assert os.path.isfile(self.settings_file)

    def test_tools_file_exists(self):
        """
        Testing to see if the tools file exists after the first run setup.
        """
        assert os.path.isfile(self.tools_file)

    def test_data_samples_exists(self):
        """
        Testing to see if the data sample files exists after the first run setup.
        """
        assert os.path.isdir(self.data_location)

    def test_tests_dir_exists(self):
        """
        Testing to see if the test directory exists after the first run setup.
        """
        assert os.path.isdir(self.tests_location)

    def test_output_dir_exists(self):
        """
        Testing if the output directory exists after running the settings manager first run setup.
        """
        assert os.path.isdir(self.output_location)

    def test_get_config_settings(self):
        """
        Testing to see if the configuration settings are valid.
        """
        given_result = SettingsManager().get_settings()
        expected_result = OrderedDict([('Locations', OrderedDict([('__name__', 'Locations'),
                                       ('tests', '${ETL_TEST_ROOT}/Documents/etlTest/tests'), ('data'
                                       , '${ETL_TEST_ROOT}/Documents/etlTest/data'), ('output',
                                       '${ETL_TEST_ROOT}/Documents/etlTest/output')])), ('Results',
                                       OrderedDict([('__name__', 'Results'), ('verbose',
                                       'True'), ('failurerate', '10'), ('reporttype', 'Normal')]))])

        self.assertCountEqual(given_result, expected_result)

    def test_get_connections(self):
        """
        Testing to ensure that the data source connections match from the configuration file.
        :return:
        """
        given_result = SettingsManager().get_connections()
        expected_result = OrderedDict([('etlUnitTest', OrderedDict([('__name__', 'etlUnitTest'),
                                                        ('hostname', '127.0.0.1'), ('username', 'root')
                                                        , ('password', ''), ('port', '3306'), ('type', 'mysql')
                                                        , ('dbname', 'etlUnitTest')]))])

        self.assertCountEqual(given_result, expected_result)

    def test_get_tools(self):
        """
        Testing to ensure that the tool configuration settings match the tool configuration file.
        """
        given_result = list(SettingsManager().get_tools())
        expected_result = [{'PDI-NoKey': {'process_param': '/file:', 'host_name': 'localhost',
                                          'code_path': '${ETL_TEST_ROOT}/etltest/samples/etl', 'port': None,
                                          'params': '/level: Detailed', 'private_key': None, 'password': None,
                                          'user_name': None, 'tool_path': '${TOOL_PATH}',
                                          'logging_filename_format': '${name}_%Y-%m-%d',
                                          'script_types': [{'script': 'kitchen.sh', 'type': 'job'},
                                                           {'script': 'pan.sh', 'type': 'trans'}]},
                            'PDI': {'process_param': '/file:', 'host_name': 'localhost',
                                    'code_path': '${ETL_TEST_ROOT}/etltest/samples/etl',
                                    'port': None, 'params': '/level: Detailed', 'private_key': '~/.ssh/id_rsa',
                                    'password': None, 'user_name': None, 'tool_path': '${TOOL_PATH}',
                                    'logging_filename_format': '${name}_%Y-%m-%d',
                                    'script_types': [{'script': 'kitchen.sh', 'type': 'job'},
                                                     {'script': 'pan.sh', 'type': 'trans'}]}}]

        self.assertCountEqual(given_result, expected_result)

    def test_get_tool(self):
        """
        Testing to ensure that etlTest gets only one Tool from the tool configuration file.
        """
        given_result = list(SettingsManager().get_tool('PDI'))
        expected_result = ['host_name', 'user_name', 'password', 'port', 'private_key', 'tool_path', 'script_types',
                           'params', 'process_param', 'code_path', 'logging_filename_format']
        self.assertCountEqual(given_result, expected_result)

    def test_find_single_setting(self):
        """
        Testing to ensure that a single setting is retrieved.
        """
        given_result = SettingsManager().find_setting('Locations', 'tests')
        expected_result = os.environ.get('ETL_TEST_ROOT') + "/Documents/etlTest/tests"

        self.assertEqual(given_result, expected_result)

    def test_fail_find_single_setting(self):
        """
        Testing that a setting that doesn't exist returns an error message.
        """
        given_result = SettingsManager().find_setting('Location', 'tests')
        expected_result = 'Setting does not exist or something went wrong.'

        self.assertEqual(given_result, expected_result)

    def test_get_file_location(self):
        """
        Testing that get_file_location returns back the root directory for etlTest.
        """
        given_result = SettingsManager().get_file_location()
        expected_result = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        expected_result = re.sub(os.path.join('etltest', 'test', 'utilities'), '', expected_result)

        self.assertEqual(given_result, expected_result)

    def test_system_variable_replace(self):
        """
        Testing that variables in a setting value are replaced with their proper value.
        """
        parameter = "${ETL_TEST_ROOT}/this_is_a_test/file.txt"
        given_result = SettingsManager().system_variable_replace(parameter)
        expected_result = str(os.environ.get('ETL_TEST_ROOT')) + "/this_is_a_test/file.txt"

        self.assertEqual(given_result, expected_result)

    def test_bad_system_variable_replace(self):
        """
        Testing that if a variable being replaced doesn't exist, an error is thrown.
        """
        parameter = "${ETL_TEST_TOOT}/this_is_a_test/file.txt"
        expected_result = "The system variable either does not exist or has a bad value. System variable: ETL_TEST_TOOT"

        with self.assertRaises(Exception) as raises:
            SettingsManager().system_variable_replace(parameter)

        self.assertEqual(str(raises.exception), expected_result)

    def test_copy_settings_file(self):
        """
        Testing that files are being copied properly with the copy_settings_file.
        """
        SettingsManager().copy_settings_file('copy.test')
        given_result = os.path.isfile(self.copy_file)
        expected_result = True

        self.assertEqual(given_result, expected_result)

    def test_no_system_variable_replace(self):
        """
        Testing that even if a variable is passed and it doesn't exist, it gets ignored.
        """
        parameter = "no_parameter/this_is_a_test/file.txt"
        given_result = SettingsManager().system_variable_replace(parameter)
        expected_result = "no_parameter/this_is_a_test/file.txt"

        self.assertEqual(given_result, expected_result)

    def test_copy_files(self):
        """
        Verifying that needed files are moved over.
        """
        given_result = os.path.isfile(os.path.join(self.data_location, "etlUnitTest/users.yml"))
        expected_result = True

        self.assertEqual(given_result, expected_result)
