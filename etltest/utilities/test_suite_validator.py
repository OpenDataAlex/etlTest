__author__ = 'ameadows'


class TestSuiteValidator():

    def __init__(self, test_suite, suites):
        """
            TestSuiteValidator is used to validate test suite functionality
            (i.e. validate that a test belongs to a test suite).
            :param test_suite The name of the test_suite to be run.
            :type test_suite str
            :param suites The group of test suites the test belongs to.
            :type suites list
        """

        self.test_suite = test_suite
        self.suites = suites

    def test_suite_validate(self):

        if self.test_suite in self.suites:
            return True
        else:
            return False