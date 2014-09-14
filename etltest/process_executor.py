__author__ = 'ameadows'
"""
    This file contains all the logic necessary to execute ETL code based on the settings stored in the tools settings
    file.  Process execution should occur after the test data is loaded and before the unit tests are run.
"""
import logging
import os
import paramiko
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
        self.log.info("Setting up tool {0:s}: {1:s}".format(tool_name, self.tool))

        self.local_names = ['localhost', '127.0.0.1']

    def create_secure_shell(self):
        """
        Create a secured shell connection to the data integration server, based on the connection info provided from
        the tool configuration file.
        :return: ssh connection.
        """
        ssh = paramiko.SSHClient()

        if ('private_key' in self.tool and self.tool['private_key'] is None) or 'private_key' not in self.tool:
            ssh.connect(self.tool['host_name'], port=self.tool['port'],
                        username=self.tool['user_name'], password=self.tool['password'])
        elif self.tool['host_name'] is not None:
            pkey = paramiko.RSAKey.from_private_key_file(self.tool['private_key'])
            ssh.set_missing_host_key_policy(paramiko.WarningPolicy())

            if self.tool['port'] is not None:
                ssh.connect(self.tool['host_name'], port=self.tool['port'], username=self.tool['user_name'],
                            password=self.tool['password'], pkey=pkey)
            else:
                ssh.connect(self.tool['host_name'], username=self.tool['user_name'],
                            password=self.tool['password'], pkey=pkey)
        else:
            raise Exception("The connection information is incorrect or not allowed.")

        return ssh

    def read_output(self, stdout, stderr):
        """
        Reads the return values of the executed process and writes them to the log.
        :param stdout:
        :param stderr:
        :return:
        """

        for line in stderr:
            self.log.error(line)

        for line in stdout:
            self.log.info(line)


    def execute_process(self, process_type, process_name):

        self.log.info("Attempting to run {0:s} with {1:s}".format(process_name, self.tool_name))

        from subprocess import call

        tool_path = SettingsManager().system_variable_replace(self.tool['tool_path'])

        process_param = self.tool['process_param']
        params = self.tool['params']
        self.log.info("Using {0:s} with {1:s}".format(process_param, params))

        process = process_param + process_name
        self.log.info("Running {0:s}".format(process))

        for type in self.tool['script_types']:
            if type['type'] == process_type:
                tool_script = type['script']

        self.log.info("Using {0:s} with {1:s}".format(tool_path, tool_script))

        tool_path_script = os.path.join(tool_path, tool_script)

        if self.tool['host_name'] not in self.local_names:
            ssh = self.create_secure_shell()

            self.log.debug("Attempting to change directory to {0:s}".format(tool_path))
            stdin, stdout, stderr = ssh.exec_command("cd " + tool_path)

            self.read_output(stdout, stderr)

            stdin, stdout, stderr = ssh.exec_command(tool_script + " " + process)

            self.read_output(stdout, stderr)
            ssh.close()
        else:

            return call([tool_path_script, process])

