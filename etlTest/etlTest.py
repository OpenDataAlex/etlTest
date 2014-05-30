"""
Main application file.  Handles options given through the command line.
"""

import sys
import optparse

__author__ = 'ameadows, coty'


def main(argv):
    """
    This class is what users call from the command line.  It will take the arguments given, validate them,
    and pass them on to the appropriate classes to continue execution.

    The main functions of the application are:
    1) Read in YAML files
    2) Generate SQLAlchemy object models on data source connections.
    3) Generate unittest tests for testing objects
    4) Execute the test code and return the results.
    """

    parser = optparse.OptionParser("usage: %prog [options]")

    # if no arguments provided, print usage instructions
    if len(argv) == 0:
        parser.print_usage()

    #all available options are defined here
    parser.add_option("-f", "--infile", dest="in_file", type="string", help="Specify the input file.")
    parser.add_option("-d", "--indir", dest="in_dir", type="string", help="Specify the input directory.")
    parser.add_option("-o", "--outdir", dest="out_dir", type="string", help="Specify the output directory.")
    parser.add_option("-s", "--schema", dest="schema_gen", type="string", help="Generate or refresh sqlalchemy schema"
                                                                               ".")
    parser.add_option("-g", "--gen", dest="gen_code", default=False, action="store_true", help="Generate new test "
                                                                                               "code.")
    parser.add_option("-e", "--exec", dest="exec_code", default=False, action="store_true", help="Execute test code.")
    parser.add_option("-t", "--test", dest="test_run", default=False, action="store_true",
                      help="Run app as tests.  Does not persist generated code or execute code.")
    (options, args) = parser.parse_args()

    # validating options
    if options.in_file and options.in_dir:
        parser.error("Options infile and indir are mutually exclusive.  Please choose one.")

    if options.schema_gen:
        from etlTest.utils.schema_generator import SchemaGenerator
        r = SchemaGenerator(options.in_file, options.in_dir)