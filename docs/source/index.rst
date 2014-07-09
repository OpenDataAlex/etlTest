.. etlTest documentation master file, created by
   sphinx-quickstart on Wed Jul  2 09:00:21 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

etlTest
=======

etlTest is a unit testing framework for testing data integration code.

The home for etlTest is on `GitHub <https://github.com/OpenDataAlex/etlTest/>`_.

The goal of etlTest is to make creating and executing unit tests for data integration code as simple as possible.  We
 have achieved this through the use of `YAML <http://www.yaml.org/>`_ files to store test data sets and the actual
 tests.  Those files then get translated into `Python unittest <https://docs.python.org/2/library/unittest.html>`_
 and can be executed from the command line and the results will show where there is more work to be done.

We are always looking for new feature requests, bugs, and other contributions!  To learn more on how to contribute,
please check out our `Contributing <https://github.com/OpenDataAlex/etlTest/blob/dev/CONTRIBUTING.md>`_ page on GitHub.

.. toctree::
   :maxdepth: 2
   :numbered:

   intro.rst
   Setting Up <setup.rst>
   Development <develop.rst>