__author__ = 'ameadows'

"""
settingsManager handles building the standard directories used by etlTest,
copies the default settings files, and building the array that stores all the parameters
from the settings files.
"""
import logging
from ConfigParser import SafeConfigParser
from shutil import copyfile, copy2

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
        self.data_dir = 'etltest/samples/data/'
        self.settings_file = etltest_config['settings_file']
        self.connection_file = etltest_config['connection_file']


        self.user_settings = appdirs.user_data_dir(self.app_name, self.app_author)
        self.user_logging = appdirs.user_log_dir(self.app_name, self.app_author)

        self.data_location = self.find_setting('Locations', 'data')

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

            self.log.debug("Data directory is %s" % os.path.isdir(self.data_location))

        else:
            self.log.info("Data directory exists (%s)" % self.data_location)

        source = os.path.join(self.get_file_location(), self.data_dir)
        dest = self.data_location
        for root, dirs, files in os.walk(source):
            for file in files:
                self.log.debug("Trying to copy %s" % file)
                s = os.path.join(root, file)
                path_part = root.replace(source, "")
                dest_full = os.path.join(dest, path_part)
                d = os.path.join(dest_full, file)

                if not os.path.isdir(dest_full):
                    self.log.debug("Building destination directory: %s" % dest_full)
                    os.makedirs(dest_full)

                if not os.path.exists(d):
                    self.log.info(u"Copying file {0:s} to {1:s}".format(s, d))
                    copy2(s, d)


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
            return ''


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