__author__ = 'coty, ameadows'

import logging
from etltest.utilities.settings import etltest_config, console
import yaml


class YAMLParser():

    def __init__(self):
        """
            Initialization of method to setup the logging.
        """

        self.log = logging.getLogger(name="YAMLParser")
        self.log.setLevel(etltest_config['logging_level'])
        self.log.addHandler(console)

    def read_file(self, filename):
        """
        Reads a single file and turns it into an array for processing.
        :param filename The name of the file to be processed.
        :type filename str
        """

        with open(filename, 'r') as f:
            data = yaml.safe_load_all(f.read())
            self.log.debug("Reading file %s." % filename)
            self.log.debug("File contents: %s ." % tuple(data))
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
                tmp = self.read_file(filename)
                yaml_results.extend(tmp)
        return yaml_results

if __name__ == "__main__":
    reader = YAMLParser().read_dir("/home/ameadows/PycharmProjects/etlTest/etltest/samples/test/")

    for r in reader:
        print r
