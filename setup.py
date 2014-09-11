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
    url='https://github.com/OpenDataAlex/etlTest',
    license='GNU GENERAL PUBLIC LICENSE Version 3',
    description='Automated and tool agnostic data integration testing tool.',
    author='Alex Meadows, Coty Sutherland',
    author_email='alexmeadows@bluefiredatasolutions.com',
    packages=find_packages(),
    install_requires=[
        'appdirs==1.3.0',
        'docutils==0.11',
        'ecdsa==0.11',
        'Jinja2==2.7.2',
        'MarkupSafe==0.19',
        'paramiko==1.14.0',
        'Pygments==1.6',
        'py==1.4.20',
        'PyYAML==3.11',
        'Sphinx==1.2.2',
        'SQLAlchemy==0.9.3',
        'subprocess32==3.2.6',
        'tox==1.7.1',
        'unittest-xml==0.2.2',
        'unittest-xml-reporting==1.9.0',
        'virtualenv==1.11.5',
        'wsgiref==0.1.2',
        'xmlunittest==0.2.0'
    ],
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Developers'
    ],
    cmdclass={'tox': Tox},
    keywords='etl data_integration testing automation',
    test_suite='etltest.test',
    entry_points={
        'console_scripts': [
            'etlTest = etltest.etlTest:main',
            'etltest = etltest.etlTest:main',
        ]
    },
    package_data={
        'etlTest': ['.etltest-settings.yml'],
    },
    data_files=[
        ('', [
                                            '.etltest-settings.yml',
                                            'CONTRIBUTING.md',
                                            'LICENSE',
                                            'README.md'
        ]),
        ('etltest/samples/data/etlUnitTest', ['etltest/samples/data/etlUnitTest/users.yml']),
        ('etltest/samples/etl', ['etltest/samples/etl/shared.xml']),
        ('etltest/samples/etl/data_mart', [
                                            'etltest/samples/etl/data_mart/user_dim_jb.kjb',
                                            'etltest/samples/etl/data_mart/user_dim_load_tr.ktr'
        ]),
        ('etltest/samples/output/DataMart', ['etltest/samples/output/DataMart/UsersDim.py']),
        ('etltest/samples/output/main', [
                                            'etltest/samples/output/main/help_arg.txt',
                                            'etltest/samples/output/main/in_dir_generation.txt',
                                            'etltest/samples/output/main/in_file_generation.txt',
                                            'etltest/samples/output/main/no_args.txt'
        ]),
        ('etltest/samples/test/dataMart', ['etltest/samples/test/dataMart/users_dim.yml']),
        ('etltest/templates/output', [
                                        'etltest/templates/output/fixture.jinja2',
                                        'etltest/templates/output/suite.jinja2',
                                        'etltest/templates/output/test.jinja2'
        ]),
        ('etltest/templates/settings', [
                                        'etltest/templates/settings/connections.cfg',
                                        'etltest/templates/settings/copy.test',
                                        'etltest/templates/settings/properties.cfg',
                                        'etltest/templates/settings/tools.yml'
        ]),
    ],
)
