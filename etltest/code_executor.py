__author__ = 'ameadows'
"""
    This file contains all the logic necessary to execute the unit test code based on the parameters passed by the user.
"""

import logging

from etltest.utilities.settings import etltest_config, console

class CodeExecutor():

    def __init__(self):
        """
            Here we initialize the CodeExecutor object, setting up the executor with custom logging and other
            parameters required.
        """

        self.log = logging.getLogger(name="CodeExecutor")
        self.log.setLevel(etltest_config['logging_level'])
        self.log.addHandler(console)

