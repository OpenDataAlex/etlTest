__author__ = 'coty, ameadows'

import logging
import os

import yaml

from etltest.utilities.settings_manager import SettingsManager


class YAMLParser():

    def __init__(self, in_file=None, in_dir=None):
        from .settings import etltest_config, console
        """
            Initialization of method to setup the logging.
        """

        self.log = logging.getLogger(name="YAMLParser")
        self.log.setLevel(etltest_config['logging_level'])
        self.log.addHandler(console)

        self.in_file = in_file
        self.in_dir = in_dir
        self.data_dir = SettingsManager().find_setting('Locations', 'data')

        if in_file is not None:
            self.read_file(self.in_file)

        if in_dir is not None:
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

    def write_file(self, data_set, source, table, column=None):
        """
        This method takes the JSON data set and parses it into a YAML file into the data directory structure.
        :param data_set: The data to be processed into a YAML file.
        :type data_set: JSON Array
        :param source: The source where the data came from.
        :type source: str
        :param table: The table from the source where the data came from.
        :type table: str
        :param column: The column that the records should be identified by within tests.  Default is to number the records.
        :type column: str
        :return:  None
        """

        count = 1
        file_path = os.path.join(self.data_dir, source)
        filename = table + '.yml'

        self.log.info('Creating {0:s} if does not exist.'.format(file_path))

        if not os.path.isdir(file_path):
            os.makedirs(file_path, mode=0o755)
            self.log.info('{0:s} created.'.format(file_path))

        os.chdir(file_path)
        self.log.info('Creating reference data file: {0:s}.'.format(filename))
        with open(filename, 'w') as f:
            # Need to take the data set one record at a time and format accordingly.
            for record in data_set:
                # Need to check if the record is identified by a column value or if we just give it an identifier.
                if column is None:
                    f.write(str(count) + ':\n')
                else:
                    f.write(str(record[column]) + ':\n')

                for column_name, column_value in record.items():
                    f.write('  ' + column_name + ': ' + str(column_value) + '\n')

                count += 1
        f.close()
