__author__ = 'coty, ameadows'

import logging
import os
from etltest.utilities.settings import etltest_config, console
from etltest.utilities.settings_manager import SettingsManager
from etltest.utilities.yaml_parser import YAMLParser


class CodeGenerator():

    def __init__(self, in_file=None, in_dir=None):
        """
        Generates full test code sets based on yaml files and the
          Jinja2 templates.
        """
        self.log = logging.getLogger(name="CodeGenerator")
        self.log.setLevel(etltest_config['logging_level'])
        self.log.addHandler(console)

        self.in_file = in_file
        self.in_dir = in_dir
        self.out_dir = SettingsManager().find_setting('Locations', 'tests')


        if self.in_file is not None:
            self.test_list = YAMLParser().read_file(self.in_file)
        elif self.in_dir is not None:
            self.test_list = YAMLParser().read_dir(self.in_dir)
        else:
            test_loc = SettingsManager().find_setting("Locations", "tests")
            self.test_list = YAMLParser.read_dir(test_loc)

    def generate_test(self):
        """
            This method generates test code based on the Jinja2 template and the test yaml file provided.
        """
        # TODO:  Continue working on YAML Validator.  Must be included either here or in the parser...

        self.jinja_setup()
        self.template = self.jinja_env.get_template("output/test.jinja2")

        for group in self.test_list:
            self.test_group, self.tests = group.popitem()
            self.file_path = self.test_group                     # Using the testGroup as the folder structure for
                                                                 # output.

            self.test_group = self.test_group.replace("\\", '')  # Removing slashes so the test class is properly
                                                                 # named.

            self.log.debug("Test Group Name: %s" % self.test_group)
            self.log.debug("Tests for test group: %s" % self.tests)


            self.data = self.generate_data(self.tests)

            self.variables = {
                "header": self.header,
                "tests": self.tests,
                "testGroup": self.test_group
                         }

            self.test_output = self.template.render(self.variables)
            os.mkdir("{}\\{}.py".format(self.out_dir, self.file_path))
            with open(self.out_dir + "\\" + self.file_path + ".py", 'w') as f:
                f.write(self.test_output)
                f.close()

    def generate_data(self, test_set):
        """
            This method takes in the dataset of a test and returns the record(s) needed to build the query.
        """
        data = []

        for test in test_set:
            return True

    def jinja_setup(self):
        from jinja2 import Environment, PackageLoader
        from time import strftime, gmtime
        self.jinja_env = Environment(loader=PackageLoader('etltest', 'templates'),
                                     trim_blocks=True, lstrip_blocks=True)

        # Header lines created here and added to the templates as required
        self.header = "#!/usr/bin/python\n" \
                 "#\n" \
                 "# This file was created by etlTest.\n#" \
                 " Create date: %s\n" \
                 "#\n" % \
                 strftime("%a, %d %b %Y %X +0000", gmtime())