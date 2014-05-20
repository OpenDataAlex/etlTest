__author__ = 'ameadows'

"""
settingsManager handles building the standard directories used by etlTest,
copies the default settings files, and building the array that stores all the parameters
from the settings files.
"""
import logging
from ConfigParser import SafeConfigParser
from shutil import copyfile
import inspect

import re
import os
import appdirs


class SettingsManager():

    def __init__(self):
        """
            This method initializes the log for SettingsManager as well as sets some static variables for file paths.
        """
        from etltest.utilities.settings import etltest_config, console

        self.log = logging.getLogger(name="SettingsManager")
        self.log.setLevel(etltest_config['logging_level'])
        self.log.addHandler(console)

        self.app_name = etltest_config['app_name']
        self.app_author = etltest_config['app_author']
        self.settings_file = etltest_config['settings_file']

        self.user_settings = appdirs.user_data_dir(self.app_name, self.app_author)
        self.user_logging = appdirs.user_log_dir(self.app_name, self.app_author)

    def first_run_test(self):
        """
        Tests if the directories used for user settings exist or not.
          No parameters are passed from outside settingsManager.
        """

        if not os.path.isdir(self.user_settings):
            self.log.info('User settings directory does not exist.  Building now.')
            os.makedirs(self.user_settings)

            self.log.info(u"Copying default settings file to user directory. ({0:s}/{1:s})".format(self
                                                                                                   .user_settings, self.settings_file))
            copyfile(self.get_file_location() + '/etltest/templates/settings/' + self.settings_file, self.user_settings
                                                                                                   + '/' + self.settings_file)

        else:
            self.log.info("User settings directory exists (%s)" % self.user_settings)

        if not os.path.isdir(self.user_logging):
            self.log.info('Logging directory does not exist.  Building now.')
            os.makedirs(self.user_logging)
        else:
            self.log.info("User logging directory exists (%s)" % self.user_logging)

    def get_settings(self):
        """
        Gets all the settings from the primary settings file (etlTest.properties).
        """
        parser = SafeConfigParser()
        return parser.read(self.user_settings + "/" + self.settings_file)

    def find_setting(self, setting_section, setting_name):
        """
        Reads the config file and returns the given setting's value.
        :param setting_section The properties file section name.
        :type setting_section str
        :param setting_name The property name
        :type setting_name str
        """
        config = self.get_settings()

        return config(setting_section)[setting_name]

    @staticmethod
    def get_file_location():

        file_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        file_path = re.sub('/etltest/utilities', '', file_path)
        return file_path