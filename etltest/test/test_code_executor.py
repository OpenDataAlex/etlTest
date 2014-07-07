__author__ = 'ameadows'

import unittest

from etltest.code_executor import CodeExecutor


class CodeExecutorTests(unittest.TestCase):

    def setUp(self):
        self.executor = CodeExecutor()

    def test_setup(self):
        # Had to create this to test if the executor would build correctly during setup.
        self.assertEqual(True, True)