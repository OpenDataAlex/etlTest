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

import os
import appdirs


class SettingsManager():

    def __init__(self):

        self.app_name = 'etlTest'
        self.app_author = 'BlueFireDS'
        self.settings_file = 'etlTest.properties'

        self.user_settings = appdirs.user_data_dir(self.app_name, self.app_author)
        self.user_logging = appdirs.user_log_dir(self.app_name, self.app_author)


    def first_run_test(self):
        """
        Tests if the directories used for user settings exist or not.
          No parameters are passed from outside settingsManager.
        """

        if not os.path.isdir(self.user_settings):
            logging.info('User settings directory does not exist.  Building now.')
            os.makedirs(self.user_settings)

            logging.info('Copying default settings files.')
            copyfile('../templates/settings/' + self.settings_file, self.user_settings + '/' + self.settings_file)

        else:
            logging.info("User settings directory exists.")

        if not os.path.isdir(self.user_logging):
            logging.info('Logging directory does not exist.  Building now.')
            os.makedirs(self.user_logging)
        else:
            logging.info("User logging directory exists")

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

    def get_file_location(self):

        return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
