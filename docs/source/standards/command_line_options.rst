Command Line Options
====================

Here are all the options provided by etlTest's command line utility: ::

    usage: etlTest [-h] [-f [IN_FILE]] [-d [IN_DIR]] [-o [OUT_DIR]]
               [-g [{all,unit,suite}]] [-e] [-t] [-v]

    Automated data integration test generator and executor.

    optional arguments:
      -h, --help            show this help message and exit
      -f [IN_FILE], --infile [IN_FILE]
                            Specify the input file
      -d [IN_DIR], --indir [IN_DIR]
                            Specify the input directory
      -o [OUT_DIR], --outdir [OUT_DIR]
                            Specify the output directory
      -g [{all,table,process}], --gen [{all,table,process}]
                            Generate new test code
      -e, --exec            Execute test code
      -t, --test            Run app as tests. Does not persist the generated or
                            executed code.
      -v, --version         show program's version number and exit

    etlTest -d /your/test_file/directory/ -g unit
    usage: etlTest [-h] [-s [SOURCE]] [-t [TABLE]] [-c [COLUMN]] [-i]
                   [-r [{ours,theirs}]]

    Reference data handler for etlTest.

    optional arguments:
      -h, --help            show this help message and exit
      -s [SOURCE], --source [SOURCE]
                            Name of the source from the connections.cfg file
      -t [TABLE], --table [TABLE]
                            Name of the table from the named source
      -c [COLUMN], --column [COLUMN]
                            Name of the key column from the named table. Used to
                            identify records.
      -i, --import          Import data from the named source table.
      -r [{ours,theirs}], --refresh [{ours,theirs}]
                            Refreshes the stored reference data. If ours, we will
                            keep our data and refresh the source. If theirs, we
                            will drop our data and refresh from the source.

    etlTest -s yourSource -t yourSourceTable -c yourTableIdentifyingColumn -i


Options Breakdown
-----------------

File Handling
`````````````
If only wanting to run a single file, use IN_FILE.  Multiple files can be processed through the usage of IN_DIR.  Both
options are mutually exclusive.

If OUT_DIR is not specified, the default output directory from the etlTest settings file will be used.

Generating tests can be done with the `--gen` or `-g` option.  It also takes one of the following values:

*  all     - builds all types of unit tests
*  table   - builds unit tests based on data source/target tables
*  process - builds unit tests based on data integration processes

Execution of tests can be done with the `--exec` or `-e` option.

Testing the test output can be done with the `--test` or `-t` option.

Reference Data Handling
```````````````````````
The ability to synchronize and maintain reference data is available in etlTest.  Based on the configured source and
table, data can either be imported or refreshed.

Source (`-s` or `--source`), table (`-t` or `--table`), and column (`-c` or `--column`) are required to generate a
reference data file.

Importing data can be done with the `--import` or `-i` option.

Refreshing data with the `--refresh` or `-r` option allows for keeping either your stored copy (`ours`) or the
source system (`theirs`) version.
