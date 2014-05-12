__author__ = 'coty, ameadows'

from etltest.utilities.settings_manager import find_setting
from etltest.utilities.yaml_parser import YAMLParser

class CodeGenerator():

    def __init__(self, in_file=None, in_dir=None):
        """
        Generates full test code sets based on yaml files and the
          Jinja2 templates.
        """
        self.in_file = in_file
        self.in_dir = in_dir

        self.env = Environment(loader=PackageLoader('etltest', 'templates'))

        if self.in_file is not None:
            self.test_list = YAMLParser.read_file(self.in_file)
        elif self.in_dir is not None:
            self.test_list = YAMLParser.read_dir(self.in_dir)
        else:
            test_loc = find_setting("Locations", "tests")
            self.test_list = YAMLParser.read_dir(test_loc)

    def generate_test(self):

    def generate_data(self):


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