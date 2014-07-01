__author__ = 'ameadows'
"""
    This file contains all the logic necessary to execute ETL code based on the settings stored in the tools settings
    file.  Process execution should occur after the test data is loaded and before the unit tests are run.
"""
import logging
import os
from etltest.utilities.settings_manager import SettingsManager

class ProcessExecutor():

    def __init__(self, tool_name):

        """
            Here we initialize the process executor object with the necessary customized logging.
            :param: tool_name The tool that is being used for running the data integration process.  This is the name of the
            tool in the tool configuration file (default is tools.yml)
            :param: tool_name str
        """
        from etltest.utilities.settings import etltest_config, console
        self.log = logging.getLogger(name="ProcessExecutor")
        self.log.setLevel(etltest_config['logging_level'])
        self.log.addHandler(console)

        self.tool_name = tool_name
        self.tool = SettingsManager().get_tool(tool_name)
        self.log.info(u"Setting up tool {0:s}: {1:s}".format(tool_name, self.tool))

    def execute_process(self, process_type, process_name):

        self.log.info(u"Attempting to run {0:s} with {1:s}".format(process_name, self.tool_name))

        from subprocess import call

        tool_path = SettingsManager().system_variable_replace('TOOL_PATH', self.tool['tool_path'])

        process_param = self.tool['process_param']
        params = self.tool['params']
        self.log.info(u"Using {0:s} with {1:s}".format(process_param, params))

        process = process_param + process_name
        self.log.info(u"Running {0:s}".format(process))

        for type in self.tool['script_types']:
            if type['type'] == process_type:
                tool_script = type['script']

        self.log.info(u"Using {0:s} with {1:s}".format(tool_path, tool_script))

        tool_path_script = os.path.join(tool_path, tool_script)

        return call([tool_path_script, process])

