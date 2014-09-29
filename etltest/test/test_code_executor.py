"""
    This module is for testing the code_executor module.
"""

__author__ = 'coty'

import unittest
import os

from etltest.code_executor import CodeExecutor


class CodeExecutorTests(unittest.TestCase):
    """
    We first have to set up some parameter for testing one file vs multiple files.
    """
    def setUp(self):
        self.one_dir_path = self.setup_oneFile()
        self.multi_dir_path = self.setup_twoFiles()

    def setup_oneFile(self):
        """
        Create a single file for testing purposes.
        """

        from tempfile import mkdtemp, mkstemp
        dir_path = mkdtemp()

        (fh, f_path) = mkstemp(suffix='.py', dir=dir_path)
        f = os.fdopen(fh, 'w')
        f.write("#!/usr/bin/python\n\nimport sys\nsys.exit(0)")
        os.chmod(f_path, 0o770)
        f.close()

        return dir_path

    def setup_twoFiles(self):
        """
        Create two temporary files for testing purposes.
        """

        from tempfile import mkdtemp, mkstemp
        dir_path = mkdtemp()

        (fh, f_path) = mkstemp(suffix='.py', dir=dir_path)
        f = os.fdopen(fh, 'w')
        f.write("#!/usr/bin/python\n\nimport sys\nsys.exit(0)")
        os.chmod(f_path, 0o770)
        f.close()

        (fh, f_path) = mkstemp(suffix='.py', dir=dir_path)
        f = os.fdopen(fh, 'w')
        f.write("#!/usr/bin/python\n\nimport sys\nsys.exit(0)")
        os.chmod(f_path, 0o770)
        f.close()

        return dir_path

    def tearDown(self):
        """
        Remove all testing files.
        """

        from shutil import rmtree
        rmtree(self.one_dir_path)
        rmtree(self.multi_dir_path)

    def test_init(self):
        """
        Testing that CodeExecutor is initialized successfully.
        """
        ce = CodeExecutor("test")
        self.assertEqual("test", ce.out_dir)

    def test_execute_one_test_mode(self):
        """
        Testing that the CodeExecutor is able to run for a single file.
        """
        ce = CodeExecutor(self.one_dir_path)
        self.assertEqual(ce.execute(True), 0)

    def test_execute_multi_test_mode(self):
        """
        Testing that the CodeExecutor is able to run for multiple files.
        """
        ce = CodeExecutor(self.multi_dir_path)
        self.assertEqual(ce.execute(True), 0)

    def test_execute_one(self):
        """
        Testing that the CodeExecutor does run for a single file.
        """
        ce = CodeExecutor(self.one_dir_path)
        self.assertEqual(ce.execute(False), None)

    def test_execute_multi(self):
        """
        Testing that the CodeExecutor does run for multiple files.
        """
        ce = CodeExecutor(self.multi_dir_path)
        self.assertEqual(ce.execute(False), None)


