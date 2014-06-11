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

    def setUp(self):
        SettingsManager().first_run_test()
        self.app_name = etltest_config['app_name']
        self.app_author = etltest_config['app_author']
        self.data_dir = appdirs.user_data_dir(self.app_name, self.app_author)
        self.log_dir = appdirs.user_log_dir(self.app_name, self.app_author)
        self.settings_file = os.path.join(self.data_dir, etltest_config['settings_file'])
        self.connection_file = os.path.join(self.data_dir, etltest_config['connection_file'])

    def test_data_dir_exists(self):
        assert os.path.exists(self.data_dir)

    def test_log_dir_exists(self):
        assert os.path.exists(self.log_dir)

    def test_settings_file_exists(self):
        assert os.path.isfile(self.settings_file)

    def test_get_config_settings(self):
        given_result = SettingsManager().get_settings()
        expected_result = OrderedDict([('Locations', OrderedDict([('__name__', 'Locations'),
                                       ('tests', '$ETL_TEST_ROOT/Documents/etlTest/tests'), ('data'
                                       , '$ETL_TEST_ROOT/Documents/etlTest/data'), ('output',
                                       '$ETL_TEST_ROOT/Documents/etlTest/output')])), ('Results',
                                       OrderedDict([('__name__', 'Results'), ('verbose',
                                       'True'), ('failurerate', '10'), ('reporttype', 'Normal')]))])

        self.assertEqual(given_result, expected_result)

    def test_get_connections(self):
        given_result = SettingsManager().get_connections()
        expected_result = OrderedDict([('etlUnitTest', OrderedDict([('__name__', 'etlUnitTest'),
                                                        ('hostname', '127.0.0.1'), ('username', 'root')
                                                        , ('password', ''), ('port', '3306'), ('type', 'mysql+pymysql')
                                                        , ('dbname', 'etlUnitTest')]))])

        self.assertEqual(given_result, expected_result)

    def test_find_single_setting(self):
        given_result = SettingsManager().find_setting('Locations', 'tests')
        expected_result = os.environ.get('ETL_TEST_ROOT') + "/Documents/etlTest/tests"

        self.assertEqual(given_result, expected_result)

    def test_fail_find_single_setting(self):
        given_result = SettingsManager().find_setting('Location', 'tests')
        expected_result = False

        self.assertEqual(given_result, expected_result)

    def test_get_file_location(self):
        given_result = SettingsManager().get_file_location()
        expected_result = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        expected_result = re.sub('/etltest/test/utilities', '', expected_result)

        self.assertEqual(given_result, expected_result)

