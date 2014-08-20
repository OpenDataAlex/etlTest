__author__ = 'coty'
"""
    This file contains all the logic necessary to execute the unit test code based on the parameters passed by the user.
"""

import logging

from utilities.settings import etltest_config, console


class CodeExecutor():

    def __init__(self, out_dir):
        """
            Here we initialize the CodeExecutor object, setting up the executor with custom logging and other
            parameters required.
        """

        self.log = logging.getLogger(name="CodeExecutor")
        self.log.setLevel(etltest_config['logging_level'])
        self.log.addHandler(console)

        self.out_dir = out_dir

    def execute(self, test_exec):
        """
        This method executes the generated tests.
        :param test_exec: Flag to determine if the tests really need to be executed or not.  If not, a list of tests
        that would be executed are shown.
        :type test_exec: boolean
        """

        from os import listdir
        from os.path import isfile, join

        # TODO: How to handle files that are not created tests? Should we list all files?

        files = [f for f in listdir(self.out_dir) if isfile(join(self.out_dir, f)) and f.endswith(".py")]

        self.log.debug(files)

        import sys
        import subprocess
        for f in files:
            file_path = "{0:s}/{1:s}".format(self.out_dir, f)

            if test_exec:
                self.log.info("Would execute {0:s}".format(file_path))
                return 0
            else:
                self.log.info(file_path)
                print subprocess.check_output([sys.executable, file_path])
