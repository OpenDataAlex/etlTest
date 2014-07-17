#!/usr/bin/python
__author__ = 'coty, ameadows'

import sys
import optparse
import argparse
from utilities.settings_manager import SettingsManager


def create_parser():
    """
    Generates a command line parser with args.
    :return: parser
    """
    parser = argparse.ArgumentParser(
        description='Automated data integration test generator and executor.',
        epilog='etlTest -d /your/test_file/directory/ -g'
    )

    parser.add_argument('-f', '--infile', nargs='?', type=str, dest='in_file', help='Specify the input file')
    parser.add_argument('-d', '--indir', nargs='?', type=str, dest='in_dir', help='Specify the input directory')
    parser.add_argument('-o', '--outdir', nargs='?', type=str, dest='out_dir', help='Specify the output directory')
    parser.add_argument('-g', '--gen', dest='gen_code', default=False, action='store_true',
                        help='Generate new test code')
    parser.add_argument('-e', '--exec', dest='exec_code', default=False, action='store_true',
                        help='Execute test code')
    parser.add_argument('-t', '--test', dest='test_run', default=False, action='store_true',
                        help='Run app as tests.  Does not persist the generated or executed code.')

    return parser


def main(argv=None):

    """
        This class is the entry point for the application. It takes the arguments, validates them, and passes
        them on to the appropriate classes to continue execution.

        Here are the main functions of this application.
        1) Take in YAML
        2) Generate code from that YAML
        3) Execute that code so that we can take advantage of the unittest libraries
    """
    parser = create_parser()
    if argv is None:
        args = sys.argv
    else:
        args = argv

    # no arguments, print usage
    if not len(sys.argv) > 1:
        parser.print_help()

    # validating args
    if args.in_file and args.in_dir:
        parser.error("Options infile and indir are mutually exclusive. Please choose one.")

    if args.gen_code:
        from code_generator import CodeGenerator

        # Has a custom output directory been set?  If not, use default.
        if args.out_dir:
            output = args.outdir
        else:
            output = SettingsManager().find_setting('Locations', 'output')


        if args.in_file:
            print(u"Attempting to process: {0:s}".format(args.in_file))
            CodeGenerator(in_file=args.in_file, out_dir=output).generate_test()

        if args.in_dir:
            print(u"Attempting to process: {0:s}".format(args.in_dir))
            CodeGenerator(in_dir=args.in_dir, out_dir=output).generate_test()

        # TODO: Decide if there should be a way to check if generated code should be updated or not.
        # TODO: Fully enable test run capability.

    if args.exec_code:
        from code_executor import CodeExecutor
        e = CodeExecutor(args.out_dir)
        e.execute(args.test_run)

if __name__ == "__main__":
    SettingsManager().first_run_test()
    parser = create_parser()
    argv = parser.parse_args()
    main(argv)