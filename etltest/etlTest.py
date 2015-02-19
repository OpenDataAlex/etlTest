"""
This is the main class for etlTest.  All other code is kicked off from here.
"""

#!/usr/bin/python
__author__ = 'coty, ameadows'

import sys
import argparse
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from etltest.utilities.settings_manager import SettingsManager
from etltest.data_connector import DataConnector
from etltest.utilities.yaml_parser import YAMLParser


def create_parser():
    """
    Generates a command line parser with args.
    :return: parser
    """
    parser = argparse.ArgumentParser(
        description='Automated data integration test generator and executor.',
        epilog='etlTest -d /your/test_file/directory/ -g unit'
    )

    parser.add_argument('-f', '--infile', nargs='?', type=str, dest='in_file', help='Specify the input file')
    parser.add_argument('-d', '--indir', nargs='?', type=str, dest='in_dir', help='Specify the input directory')
    parser.add_argument('-o', '--outdir', nargs='?', type=str, dest='out_dir', help='Specify the output directory')
    parser.add_argument('-g', '--gen', nargs='?', type=str, choices=['all', 'unit', 'suite'], dest='gen_code',
                        default='all', help='Generate new test code')
    parser.add_argument('-e', '--exec', dest='exec_code', default=False, action='store_true',
                        help='Execute test code')
    parser.add_argument('-t', '--test', dest='test_run', default=False, action='store_true',
                        help='Run app as tests.  Does not persist the generated or executed code.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1.6 - Beta')

    # subparsers = parser.add_subparsers(title="Sub Processes",
    #                                    description="Sub-processes for etlTest",
    #                                    dest='subparser_name')
    # subparsers.required = False

    return parser


def create_parser_ref():
    """
    Create argparser parser for reference data handling.
    :return: parser_ref parser object
    """
    # Create parser for handling reference data for tests.
    parser_ref = argparse.ArgumentParser(
        description='Reference data handler for etlTest.',
        epilog='etlTest -s yourSource -t yourSourceTable -c yourTableIdentifyingColumn -i'
    )
    parser_ref.add_argument('-s', '--source', nargs='?', type=str, dest='source',
                            help='Name of the source from the connections.cfg file')
    parser_ref.add_argument('-t', '--table', nargs='?', type=str, dest='table',
                            help='Name of the table from the named source')
    parser_ref.add_argument('-c', '--column', nargs='?', type=str, dest='column',
                            help='Name of the key column from the named table.  Used to identify records.')
    parser_ref.add_argument('-i', '--import', dest='import_data', default=False, action='store_true',
                            help='Import data from the named source table.')
    parser_ref.add_argument('-r', '--refresh', nargs='?', type=str, choices=['ours', 'theirs'], dest='refresh_data',
                            help='Refreshes the stored reference data.  If ours, we will keep our data and refresh the '
                                 'source.  If theirs, we will drop our data and refresh from the source.')

    return parser_ref


def main():

    """
        This class is the entry point for the application. It takes the arguments, validates them, and passes
        them on to the appropriate classes to continue execution.

        Here are the main functions of this application.
        1) Take in YAML
        2) Generate code from that YAML
        3) Execute that code so that we can take advantage of the unittest libraries
        4) Handle reference data from sources/targets that needs to be kept in sync
    """
    parser = create_parser()
    parser_ref = create_parser_ref()
    args, extra = parser.parse_known_args()
    ref_args, ref_extra = parser_ref.parse_known_args()

    # no arguments, print usage
    if len(sys.argv) < 2:
        parser.print_help()
        parser_ref.print_help()

    if 'ref' in extra:
        # We require a source connection to work with.
        if args.source is None:
            parser.error("A source is required to work with reference data.  "
                         "Please provide an existing data source.")

        # We also need a table name to pull data from.
        if ref_args.table is None:
            parser.error("A source table is required to work with reference data.  "
                         "Please provide an existing reference table.")

        # It's okay if a column is not specified for identifying the records.  We'll number them.

        # The primary function of the reference handler is to import data from a source and store it as a YAML file.
        if ref_args.import_data or ref_args.refresh_data == 'theirs':
            # First we need to build our data set.  Pulling the data.
            print(u"Reading data from {0:s}.{1:s}".format(ref_args.source, ref_args.table))

            data_set = DataConnector(ref_args.source).select_data("all_columns", ref_args.table)

            # Now we need to process the data and turn it into a YAML file.

            print(u"Generating YAML file {0:s}/{1:s}.yml using {2:s} as the record identifier.".format(ref_args.source,
                                                                                                       ref_args.table,
                                                                                                       ref_args.column))
            YAMLParser().write_file(data_set, ref_args.source, ref_args.table, ref_args.column)

        if ref_args.refresh_data == 'ours':
            # We need to take our reference data file and try to load it into the data target.

            # First we need to truncate the table.
            print(u"Truncate table {0:s}.{1:s}".format(ref_args.source, ref_args.table))
            DataConnector(ref_args.source).truncate_data(ref_args.table)

            # And now we can load all our data from the reference data file.
            print(u"Loading data from reference data file.")
            DataConnector(ref_args.source).insert_data(ref_args.table)

    else:
        # validating args
        if args.in_file and args.in_dir:
            parser.error("Options infile and indir are mutually exclusive. Please choose one.")

        # Has a custom output directory been set?  If not, use default.
        if args.out_dir:
            out_dir = args.out_dir
        else:
            out_dir = SettingsManager().find_setting('Locations', 'output')

        if args.gen_code:
            from code_generator import CodeGenerator

            if args.in_file:
                print(u"Attempting to process: {0:s}".format(args.in_file))
                CodeGenerator(in_file=args.in_file, out_dir=out_dir).generate_tests(args.gen_code)

            if args.in_dir:
                print(u"Attempting to process: {0:s}".format(args.in_dir))
                CodeGenerator(in_dir=args.in_dir, out_dir=out_dir).generate_tests(args.gen_code)

            # TODO: Decide if there should be a way to check if generated code should be updated or not.
            # TODO: Fully enable test run capability.

        if args.exec_code:
            from code_executor import CodeExecutor
            e = CodeExecutor(out_dir)
            e.execute(args.test_run)

if __name__ == "__main__":
    SettingsManager().first_run_test()
    main()