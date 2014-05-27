__author__ = 'ameadows'

import unittest
import os
import appdirs
from collections import OrderedDict

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

    def test_data_dir_exists(self):
        assert os.path.exists(self.data_dir)

    def test_log_dir_exists(self):
        assert os.path.exists(self.log_dir)

    def test_settings_file_exists(self):
        assert os.path.isfile(self.settings_file)

    def test_get_config_settings(self):
        given_result = SettingsManager().get_settings()
        expected_result = OrderedDict([('Locations', OrderedDict([('__name__', 'Locations'),
                                       ('tests', '~\\Documents\\etlTest\\tests'), ('data'
                                       , '~\\Documents\\etlTest\\data'), ('output',
                                       '~\\Documents\\etlTest\\output')])), ('Results',
                                       OrderedDict([('__name__', 'Results'), ('verbose',
                                       'True'), ('failurerate', '10'), ('reporttype', 'Normal')]))])

        self.assertEqual(given_result, expected_result)

    def test_find_single_setting(self):
        given_result = SettingsManager().find_setting('Locations', 'tests')
        expected_result = "~\\Documents\\etlTest\\tests"

        self.assertEqual(given_result, expected_result)

    def test_fail_find_single_setting(self):
        given_result = SettingsManager().find_setting('Location', 'tests')
        expected_result = False

        self.assertEqual(given_result, expected_result)


