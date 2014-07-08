__author__ = 'ameadows, coty'

import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import etltest


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)

setup(
    name='etlTest',
    version=etltest.__version__,
    url='',
    license='GNU GENERAL PUBLIC LICENSE Version 3',
    description='',
    author='Alex Meadows, Coty Sutherland',
    packages=find_packages(),
    install_requires=[
        'appdirs==1.3.0',
        'Jinja2==2.7.2',
        'MarkupSafe==0.19',
        'MySQL-python==1.2.5',
        'PyYAML==3.11',
        'Pygments==1.6',
        'SQLAlchemy==0.9.3',
        'Sphinx==1.2.2',
        'docutils==0.11',
        'py==1.4.20',
        'tox==1.7.1',
        'unittest-xml==0.2.2',
        'unittest-xml-reporting==1.7.0',
        'virtualenv==1.11.5',
        'wsgiref==0.1.2',
        'xmlunittest==0.2.0'
    ],
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta'
        'Natural Language :: English',
    ],
    cmdclass = {'tox': Tox},
    test_suite='etltest.test'
)
