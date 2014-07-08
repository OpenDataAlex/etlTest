__author__ = 'coty, ameadows'

import logging
import yaml


class YAMLParser():

    def __init__(self, in_file=None, in_dir=None):
        from settings import etltest_config, console
        """
            Initialization of method to setup the logging.
        """

        self.log = logging.getLogger(name="YAMLParser")
        self.log.setLevel(etltest_config['logging_level'])
        self.log.addHandler(console)

        self.in_file = in_file
        self.in_dir = in_dir

        if in_file != None:
            self.read_file(self.in_file)

        if in_dir != None:
            self.read_dir(self.in_dir)

    def read_file(self, filename):
        """
        Reads a single file and turns it into an array for processing.
        :param filename The name of the file to be processed.
        :type filename str
        """

        with open(filename.strip(), 'r') as f:
            data = yaml.safe_load_all(f.read())
            self.log.debug("Reading file %s." % filename)
            return data

    def read_dir(self, dirname):
        """
        Reads in the directory and then processes it through all subdirectories until all files
        have been processed.
        :param dirname The name of the directory
        :type dirname str
        """

        yaml_results = []  # Full listing of all yaml file contents from the dirname.
        self.log.debug("Reading directory %s." % dirname)

        from os import walk
        for root, subFolders, files in walk(dirname):
            for file in files:
                filename = root + "/" + file
                self.log.debug("Processing file %s " % filename)
                yaml_results.extend(self.read_file(filename))
        return yaml_results
