"""
CodeGenerator handles the creation of code based on Jinja2 templates.
"""
__author__ = 'coty, ameadows'

import logging
import os

from .utilities.settings import etltest_config, console
from .utilities.settings_manager import SettingsManager
from .utilities.yaml_parser import YAMLParser


class CodeGenerator():
    """
    This class reads in yaml files and processes them into executable Python code.
    """

    def __init__(self, in_file=None, in_dir=None, out_dir=None, test_run=None):
        """
        Generates full test code sets based on yaml files and the
          Jinja2 templates.  in_file and in_dir are mutually exclusive.
        :param in_file:  The single file to be processed.  Can not be set if in_dir is set.
        :param in_file:  str
        :param in_dir:  The directory to be processed.  Can not be set if in_file is set.
        :param in_dir:  str
        """
        self.log = logging.getLogger(name="CodeGenerator")
        self.log.setLevel(etltest_config['logging_level'])
        self.log.addHandler(console)

        self.in_file = in_file
        self.in_dir = in_dir
        self.out_dir = out_dir

        self.test_dir = SettingsManager().find_setting('Locations', 'tests')
        self.data_dir = SettingsManager().find_setting('Locations', 'data')

        #Read a single file
        if self.in_file is not None:
            self.test_list = YAMLParser().read_file(self.in_file)

        #Unless it's a directory
        elif self.in_dir is not None:
            self.test_list = YAMLParser().read_dir(self.in_dir)

        #But if nothing is passed, read everything in the test directory
        else:
            test_loc = SettingsManager().find_setting("Locations", "tests")
            self.test_list = YAMLParser().read_dir(test_loc)

        #If the output directory is not specified, use the default.
        if self.out_dir is None:
            self.out_dir = SettingsManager().find_setting('Locations', 'output')

    def generate_tests(self, generate_type):
        """
        Based on user input, generate tests based on the generation type.  The value 'all' will run through all other
        test types and generate code accordingly.
        :param generate_type: The type of tests that will be generated.  'All' will generate all other test types.
        :type generate_type: str
        """

        if generate_type == 'table':
            self.generate_test('table')
        elif generate_type == 'process':
            self.generate_test('process')
        else:  # This is the 'all' case.  Default is to run all test types.
            self.generate_test('table')
            self.generate_test('process')

    def generate_test(self, template_type):
        """
            This method generates test code based on the Jinja2 template and the test yaml file provided.
        :param template_type:  The name of the template type that is to be used.
        :type template_type: string
        """
        # TODO:  Continue working on YAML Validator.  Must be included either here or in the parser...

        self.jinja_setup()
        template_file = self.get_template(template_type)

        self.log.info("Creating tests of type: {0:s}".format(template_type))

        template = self.jinja_env.get_template("output/" + template_file)

        #We must break out each test and generate the test file for it.
        for group in self.test_list:
            self.test_group, self.tests = group.popitem()
            self.file_path, self.filename = self.test_group.rsplit("\\", 1)      # Using the testGroup as the
            self.filename += ".py"                                               # folder structure for output.
            self.file_path = os.path.join(self.out_dir, self.file_path)
            self.test_group = self.test_group.replace("\\", '')  # Removing slashes so the test class is properly
                                                                 # named.

            self.log.debug("Test Group Name: %s" % self.test_group)
            self.log.debug("Tests for test group: %s" % self.tests)
            self.log.debug("File path: %s" % self.file_path)
            self.log.debug("File name: %s" % self.filename)

            self.variables = {
                                "header": self.header,
                                "tests": self.tests,
                                "testGroup": self.test_group
                             }

            if not os.path.isdir(self.file_path):
                os.makedirs(self.file_path, 0o755)
                self.log.debug("%s directory created." % self.file_path)

            os.chdir(self.file_path)
            with open(self.filename, 'w') as f:
                f.write(template.render(self.variables))
                f.close()

            self.log.info("{0:s} test file generated.".format(self.filename))

    def get_template(self, template_type=None):
        """
        This method returns back the template file name based on the type of template needed.
        :param template_type: The type of template required.
        :type template_type: str
        :return template_name str The name of the template file.
        """
        template_name = 'table.jinja2'  # Return the default value if no test types are passed.

        if template_type == 'table':
            template_name = 'table.jinja2'
        elif template_type == 'process':
            template_name = 'process.jinja2'

        return template_name

    def jinja_setup(self):
        """
        Creates the header and setup for Jinja to process the yaml data.
        """

        from jinja2 import Environment, FileSystemLoader

        template_dir = os.path.join(SettingsManager().get_file_location(), 'etltest/templates')

        self.log.debug("Attempting to process templates from {0:s}".format(template_dir))

        self.jinja_env = Environment(loader=FileSystemLoader(template_dir),
                                     trim_blocks=True, lstrip_blocks=True)

        # Header lines created here and added to the templates as required
        self.header = "#!/usr/bin/python\n" \
                 "#\n" \
                 "# This file was created by etlTest.\n" \
                 "#\n"