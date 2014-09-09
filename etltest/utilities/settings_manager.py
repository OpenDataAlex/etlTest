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
        from settings import etltest_config, console

        self.log = logging.getLogger(name="SettingsManager")
        self.log.setLevel(etltest_config['logging_level'])
        self.log.addHandler(console)
        self.log.debug(u"Settings imported: {0:s}".format(etltest_config))
        self.app_name = etltest_config['app_name']
        self.app_author = etltest_config['app_author']
        self.data_dir = 'etltest/samples/data/'
        self.test_dir = 'etltest/samples/test/'
        self.settings_file = etltest_config['settings_file']
        self.connection_file = etltest_config['connection_file']
        self.tools_file = etltest_config['tools_file']


        self.variable_pattern = "\$\{.{0,10000}\}"

        self.user_settings = appdirs.user_data_dir(self.app_name, self.app_author)
        self.user_logging = appdirs.user_log_dir(self.app_name, self.app_author)

        self.path_loc = '/etltest/templates/settings/'

    def first_run_test(self):
        """
            Tests if the directories used for user settings exist or not.
              No parameters are passed from outside settingsManager.
        """

        if not os.path.isdir(self.user_settings):
            self.log.info('User settings directory does not exist.  Building now.')
            os.makedirs(self.user_settings)
            self.copy_settings_file(self.settings_file)
            self.copy_settings_file(self.connection_file)
            self.copy_settings_file(self.tools_file)

        else:
            self.log.info("User settings directory exists (%s)" % self.user_settings)

        self.make_dir(self.user_logging)

        data_location = self.find_setting('Locations', 'data')
        self.make_dir(data_location)

        test_location = self.find_setting('Locations', 'tests')
        self.make_dir(test_location)

        output_location = self.find_setting('Locations', 'output')
        self.make_dir(output_location)

        data_source = os.path.join(self.get_file_location(), self.data_dir)
        data_dest = data_location
        #Copying sample data files.
        self.copy_files(data_source, data_dest)

        test_source = os.path.join(self.get_file_location(), self.test_dir)
        test_dest = test_location
        #Copying sample test files.
        self.copy_files(test_source, test_dest)

    def copy_files(self, source, dest):
        """
        Takes files from the source and copies them to the destination directory.
        :param source: The source directory of the files.
        :type source: str
        :param dest:  Where the files need to be copied to.
        :type dest:  str
        """

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

    def make_dir(self, dir):
        """
        Takes the given directory path and ensures that it exists.  If not, it will create it.
        :param dir: Directory path needing to be tested/created.
        :type dir: str
        """
        if not os.path.isdir(dir):
            self.log.info("Directory does not exist.  Building now.")
            os.makedirs(dir)
            self.log.debug("Directory is %s" % dir)
        else:
            self.log.debug("Directory exists (%s)" % dir)

    def get_settings(self):
        """
            Gets all the settings from the primary settings file (properties.cfg).
        """
        return self.read_settings_file(self.settings_file)

    def get_connections(self):
        """
            Gets all the connections from the primary connections file (connections.cfg).
        """

        return self.read_settings_file(self.connection_file)

    def get_tools(self):
        """
            Gets all the tools from the primary tools file (tools.yml)
        """

        from etltest.utilities.yaml_parser import YAMLParser

        return YAMLParser().read_file(os.path.join(self.user_settings, self.tools_file))

    def get_tool(self, tool_name):

        tools = self.get_tools()

        while True:
            tool = tools.next()

            if tool[tool_name]:
                return tool[tool_name]

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
            return self.system_variable_replace(config_var)
        except Exception:
            return "Setting does not exist or something went wrong."

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

    def system_variable_replace(self, parameter):
        """
            Takes the given parameter and checks to see if any system_variable in it exists on the system and then
            replaces the variable name with the value of the variable.
            :param parameter: The parameter needing to have a system variable replaced in (i.e. tool_path, code_path, etc.)
            :type parameter: str
            :return: Value of the parameter with all variables replaced.
        """
        variable_list = re.findall(self.variable_pattern, parameter)
        self.log.debug(u"Variable list:  {0:s}".format(variable_list))
        modified_param = str()
        for system_variable in variable_list:
            system_variable = re.sub('[\$\{\}]', '', system_variable)
            variable_value = str(os.environ.get(system_variable))

            self.log.debug(u"Found {0:s} and it has a value of {1:s}".format(system_variable, variable_value))

            if variable_value == "None":
                raise Exception(u"The system variable either does not exist or has a bad value. System variable: "
                                 u"{0:s}".format(system_variable))
            else:
                self.log.debug(u"Replacing ${0:s} with {1:s}".format(system_variable,
                               variable_value))
                modified_param = parameter.replace("${" + system_variable + "}", variable_value)
            self.log.debug(u"Final parameter value is: {0:s}".format(modified_param))
        if modified_param == '':
            return parameter
        else:
            return modified_param

    def copy_settings_file(self, filename):
        """
            Adds an alert to the log and then copies the file to the setting directory.
        :param filename:  The name of the file to be copied.
        :type filename: str
        """

        self.log.info(u"Copying default settings file to user directory. ({0:s}/{1:s})".format(self.user_settings,
                                                                                    filename))

        copyfile(self.get_file_location() + self.path_loc + filename,
                 self.user_settings + '/' + filename)