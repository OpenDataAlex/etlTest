__author__ = 'ameadows'
"""
    This file contains all the logic necessary to execute ETL code based on the settings stored in the tools settings
    file.  Code execution should occur after the test data is loaded and before the unit tests are run.
"""

from etltest.utilities.settings import etltest_config, console

class CodeExecutor():

    def __init__(self):
        """
            Here we initialize the CodeExecutor object, setting up the executor per the settings in the tool settings
            file.
        """

        self.log = logging.getLogger(name="CodeExecutor")
        self.log.setLevel(etltest_config['logging_level'])
        self.log.addHandler(console)

