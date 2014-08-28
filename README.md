#etlTest

[![Build Status](https://travis-ci.org/OpenDataAlex/etlTest.png?branch=dev)](https://travis-ci.org/OpenDataAlex/etlTest)
[![Coverage Status](https://coveralls.io/repos/OpenDataAlex/etlTest/badge.png?branch=dev)](https://coveralls.io/r/OpenDataAlex/etlTest?branch=dev)
[![Documentation Status](https://readthedocs.org/projects/etltest/badge/?version=latest)](https://readthedocs.org/projects/etltest/?badge=latest)

[![endorse](https://api.coderwall.com/dbaalex/endorsecount.png)](https://coderwall.com/dbaalex)

##Installation

You can install **etlTest** by downloading the source and using the setup.py script as follows:

    $ git clone git@github.com:OpenDataAlex/etlTest.git
    $ cd etlTest
    $ python setup.py install

This setup call installs all of the necessary python dependencies. There are a few external dependencies as well, so please see the section below labeled "Non-Python Dependencies".

Once you have done that, its ready to run!

### So what is etlTest?

Having come from software development and working with data integration tools, we always wondered why there wasn't 
some kind of uniform unit and integration testing tool specific to data integration.  etlTest aims to fill that gap 
by providing an easy to use tool and data source agnostic testing tool.  Testing is designed to be "black box" - 
which means that we aren't diving into the actual data integration code.  Rather, 
we are executing the data integration process based on test data sets provided by the test writer and comparing the 
results using Python's unittest framework.

etlTest is based on the work and discussions that were started with etlUnit.

### Quickstart

To actually use etlTest, you need a data and test file for it to act on. A most basic resource file can be 
found in 
the [samples](https://github.com/OpenDataAlex/etlTest/tree/dev/etltest/samples) directory of the project 
(data/etlUnitTest/users.yml and test/dataMart/users_dim.yml). 
Executing the
 following will take that resource, generate some python code in the output directory specified, and run the code which will display the output of the tests executed to your terminal.

    $ python etlTest/etltest/etlTest.py -f <path to users_dim.yml test file> -o /tmp/ -g -e

### Documentation

The documentation for **etlTest** can be found on Read the Docs [here](https://etlTest.readthedocs.org/en/latest/).

### Non-Python Dependencies

The only dependencies that are not handled in python currently are the ones for SQLAlchemy to connect to datasources. Documentation on how to install these is as follows:

* [MySQL](https://github.com/OpenDataAlex/etlTest/blob/develop/docs/mysql_deps.md)
* [Oracle](https://github.com/OpenDataAlex/etlTest/blob/develop/docs/oracle_deps.md)

### Reporting Issues

We would love some feedback! Please do not hesitate to report any issues/questions/comments via the [Github Issue Tracker](https://github.com/OpenDataAlex/etlTest/issues).
