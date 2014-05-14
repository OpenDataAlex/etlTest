__author__ = 'ameadows'

import unittest

from etltest.utilities.settings_manager import SettingsManager


class SettingsManagerTest(unittest.TestCase):

    def setUp(self):
        SettingsManager().first_run_test()

    def test_settings_setup(self):

        return True