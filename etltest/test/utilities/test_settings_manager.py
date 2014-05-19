__author__ = 'ameadows'

import unittest
import os
import appdirs

from etltest.utilities.settings import etltest_config
from etltest.utilities.settings_manager import SettingsManager


class SettingsManagerTest(unittest.TestCase):

    def setUp(self):
        SettingsManager().first_run_test()

    def test_settings_setup(self):
        app_name = etltest_config['app_name']
        app_author = etltest_config['app_author']
        settings_file = etltest_config['settings_file']
        data_dir = appdirs.user_data_dir(app_name, app_author)
        log_dir = appdirs.user_log_dir(app_name, app_author)
        settings_file = data_dir + "/" + settings_file

        assert os.path.exists(data_dir)
        assert os.path.exists(log_dir)
        assert os.path.exists(settings_file)

