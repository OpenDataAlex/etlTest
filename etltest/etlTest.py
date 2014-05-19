__author__ = 'coty, ameadows'

import sys
import optparse

from etltest.utilities.settings_manager import SettingsManager


def main(argv):

    """
        This class is the entry point for the application. It takes the arguments, validates them, and passes
        them on to the appropriate classes to continue execution.

        Here are the main functions of this application.
        1) Take in YAML
        2) Generate code from that YAML
        3) Execute that code so that we can take advantage of the unittest libraries
    """
    parser = optparse.OptionParser("usage: %prog [options]")
    SettingsManager().first_run_test()

    # no arguments, print usage
    if len(argv) == 0:
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
        from etltest.utilities.yaml_parser import YAMLReader
        r = YAMLReader(in_file=options.in_file, in_dir=options.in_dir)
        resource_data = r.readTests()

        from etltest.code_generator import CodeGenerator
        g = CodeGenerator(options.out_dir, resource_data, options.test_run)
        # TODO: Decide if there should be a way to check if generated code should be updated or not.
        g.generateCode()

    if options.exec_code:
        from etltest.code_executor import CodeExecutor
        e = CodeExecutor(options.out_dir)
        e.execute(options.test_run)

if __name__ == "__main__":
    main(sys.argv[1:])