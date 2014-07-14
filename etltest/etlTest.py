#!/usr/bin/python
__author__ = 'coty, ameadows'

import sys
import optparse

from utilities.settings_manager import SettingsManager


def main():

    """
        This class is the entry point for the application. It takes the arguments, validates them, and passes
        them on to the appropriate classes to continue execution.

        Here are the main functions of this application.
        1) Take in YAML
        2) Generate code from that YAML
        3) Execute that code so that we can take advantage of the unittest libraries
    """
    parser = optparse.OptionParser("usage: %prog [options]")
    argv = sys.argv[1:]
    SettingsManager().first_run_test()

    # no arguments, print usage
    if len(parser.parse_args()) == 0:
        parser.print_usage()

    # all available options are defined here
    parser.add_option("-f", "--infile", dest="in_file", type="string", help="Specify the input file.")
    parser.add_option("-d", "--indir", dest="in_dir", type="string", help="Specify the input directory.")
    parser.add_option("-o", "--outdir", dest="out_dir", type="string", help="Specify the output directory.")
    parser.add_option("-g", "--gen", dest="gen_code", default=False, action="store_true",
                      help="Generate new test code.")
    parser.add_option("-e", "--exec", dest="exec_code", default=False, action="store_true",
                      help="Execute test code.")
    parser.add_option("-t", "--test", dest="test_run", default=False, action="store_true",
                      help="Run app as tests. Does not persist generated code or execute code.")
    (options, args) = parser.parse_args()



    # validating options
    if options.in_file and options.in_dir:
        parser.error("Options infile and indir are mutually exclusive. Please choose one.")

    if options.gen_code:
        from code_generator import CodeGenerator

        # Has a custom output directory been set?  If not, use default.
        if options.out_dir:
            output = options.outdir
        else:
            output = SettingsManager().find_setting('Locations', 'output')


        if options.in_file:
            print(u"Attempting to process: {0:s}".format(options.in_file))
            CodeGenerator(in_file=options.in_file, out_dir=output).generate_test()

        if options.in_dir:
            print(u"Attempting to process: {0:s}".format(options.in_dir))
            CodeGenerator(in_dir=options.in_dir, out_dir=output).generate_test()

        # TODO: Decide if there should be a way to check if generated code should be updated or not.
        # TODO: Fully enable test run capability.

    if options.exec_code:
        from code_executor import CodeExecutor
        e = CodeExecutor(options.out_dir)
        e.execute(options.test_run)

if __name__ == "__main__":
    main()