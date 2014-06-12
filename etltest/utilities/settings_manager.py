__author__ = 'ameadows'

"""
settingsManager handles building the standard directories used by etlTest,
copies the default settings files, and building the array that stores all the parameters
from the settings files.
"""
import logging
from ConfigParser import SafeConfigParser
from shutil import copyfile

import re
import os
import appdirs
import shutil


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
        self.data_dir = 'samples/data/'
        self.settings_file = etltest_config['settings_file']
        self.connection_file = etltest_config['connection_file']
        self.data_location = self.find_setting('Locations', 'data')


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

            self.log.info(u"Copying default settings file to user directory. ({0:s}/{1:s})".format(self.user_settings
                          , self.settings_file))
            copyfile(self.get_file_location() + '/etltest/templates/settings/' + self.settings_file, self.user_settings
                     + '/' + self.settings_file)

            self.log.info(u"Copying default connection file to user directory. ({0:s}/{1:s})".format(self.user_settings
                          , self.connection_file))
            copyfile(self.get_file_location() + '/etltest/templates/settings/' + self.connection_file,
                     self.user_settings + '/' + self.connection_file)

        else:
            self.log.info("User settings directory exists (%s)" % self.user_settings)

        if not os.path.isdir(self.user_logging):
            self.log.info('Logging directory does not exist.  Building now.')
            os.makedirs(self.user_logging)
        else:
            self.log.info("User logging directory exists (%s)" % self.user_logging)

        if not os.path.isdir(self.data_location):
            self.log.info("Data directory does not exist.  Building now.")
            os.makedirs(self.data_location)

            self.log.info(u"Copying sample data files to user directory. ({0:s}/{1:s})".format(self.user_settings
              , self.data_dir))
            shutil.copytree(self.get_file_location() + '/etltest/' + self.data_dir,
            self.data_location)
        else:
            self.log.info("Data directory exists (%s)" % self.data_location)


    def get_settings(self):
        """
            Gets all the settings from the primary settings file (etlTest.properties).
        """
        return self.read_settings_file(self.settings_file)


    def get_connections(self):
        """
            Gets all the connections from the primary connections file (etlTest.connections).
        """

        return self.read_settings_file(self.connection_file)

    def find_setting(self, setting_section, setting_name):
        """
            Reads the config file and returns the given setting's value.
            :param setting_section: The properties file section name.
            :type setting_section: str
            :param setting_name: The property name
            :type setting_name: str
        """
        config = self.get_settings()

        try:
            config_var = config[setting_section][setting_name]
            etl_test_root = str(os.environ.get('ETL_TEST_ROOT'))
            if "$ETL_TEST_ROOT" in config_var:
                self.log.debug("Replacing ETL_TEST_ROOT with %s" % etl_test_root)
                return config_var.replace("$ETL_TEST_ROOT", etl_test_root)
            else:
                return config_var
        except Exception:
            return False


    @staticmethod
    def get_file_location():

        file_path = os.path.dirname(os.path.abspath(__file__))
        file_path = re.sub('/etltest/utilities', '', file_path)

        return file_path

    def read_settings_file(self, settings_file):
        """
            Parses file using the SafeConfigParser.  Will return the file as an array.
            :param settings_file: The file to be processed.
            :type settings_file:  str
            :returns: Array
        """
        parser = SafeConfigParser()
        parser.read(os.path.join(self.user_settings, settings_file))
        self.log.info(parser._sections)
        return parser._sections