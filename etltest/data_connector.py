__author__ = 'coty, ameadows'
"""
    This file contains all the logic to connect to data sources using SQLAlchemy.
"""

import logging

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table, inspect
from etltest.utilities.settings import etltest_config, console
from etltest.utilities.yaml_parser import YAMLParser


class DataConnector():
    #TODO:  Need to determine if a data validation tool is required.  For instance, does record set match the table
    # structure?
    def __init__(self, conn_name):
        """
            This function initializes the data source connection so that data can be CRUDed.

            :param conn_name:  The name of the connection that the test suites reference.  This should match a
                                connection name from the connections settings file (default etlTest.connections).
            :type conn_name: str
        """
        from etltest.utilities.settings_manager import SettingsManager

        self.log = logging.getLogger(name="DataConnector")
        self.log.setLevel(etltest_config['logging_level'])
        self.log.addHandler(console)

        self.conn_name = conn_name
        self.data_dir = SettingsManager().find_setting('Locations', 'data')

        connections = SettingsManager().get_connections()
        connection = connections[self.conn_name]

        if connection is None:
            self.log.error("Connection %s does not exist, exiting." % conn_name)
            exit()

        self.engine = create_engine('{}://{}:{}@{}:{}/{}'.format(
            connection['type'],
            connection['username'],
            connection['password'],
            connection['hostname'],
            connection['port'],
            connection['dbname']
        ))

        self.meta = MetaData()
        self.insp = inspect(self.engine)

        session = sessionmaker(bind=self.engine)
        self.session = session()

        self.conn = self.engine.connect()

    def get_table(self, table_name):
        """
            This method gets a table from the data connection using SQLAlchemy's reflection capability.
            :param table_name: The name of the table being reflected.
            :param table_name: str
            :returns:  SQLAlchemy Table object
        """
        table = Table(table_name, self.meta)
        self.log.debug("Reflecting table %s" % table_name)
        self.insp.reflecttable(table, None)

        return table

    def insert_data(self, table_name, record_set):
        """
            This method inserts records into the given table for the specified connection.
            :param table_name: Name of the table we want to insert data into.
            :param table_name: str
            :param record_set: An array of record keys to retrieve the records to insert.
            :param record_set: arr
        """

        table = self.get_table(table_name)
        data = self.generate_data(table_name, record_set)
        insert = table.insert().values(data)
        self.log.debug("Inserting records for table %s (%s)" % table_name, record_set)

        self.conn.execute(insert)

    def truncate_data(self, table_name):
        #TODO: Need another method to only delete inserted records.  Only use this on single user environments.
        """
            This method deletes records from the given table by truncating the table.
            :param table_name:  Name of the table to be truncated.
            :param table_name:  str
        """
        table = self.get_table(table_name)
        delete = table.delete()
        self.log.debug("Truncating table %s." % table_name)

        self.conn.execute(delete)

    def select_data(self, table_name, columns, filter):
        #TODO:  How to handle complex WHERE clauses?
        #TODO:  Should we support sub-selects?
        #TODO:  Should we support joins?
        """
            This method queries records from the given table based on particular columns desired and the required
            filter criteria.
            :param table_name:  Name of the table to be queried (FROM clause).
            :param table_name: str
            :param columns:  Names of the columns to be returned from the query (SELECT clause).
            :param columns: arr
            :param filter:  The filter criteria for the query (WHERE clause)
            :param filter:  arr
        """

        table = self.get_table(table_name)
        result = self.session.query(table).all()

        return self.to_json(result, table)

    def generate_data(self, table_name, records):
        """
        :param table_name: Name of the table yaml file that will be retrieved.
        :param table_name: str
        :param records: The set of keys for the records that need to be retrieved and inserted into the connection.
        :param records: arr
        :return: Formatted data set for the the data connector method.
        """

        full_set = list(YAMLParser().read_file(self.data_dir + "/" + self.conn_name + "/" + table_name + ".yml"))
        subset = []
        for record in records:
            subset.extend(full_set[record])
        return subset

    def encrypt_password(self, plain_pass, salt):
        from passlib.hash import sha256_crypt

        return sha256_crypt.encrypt(plain_pass, salt)

    def to_json(self, result_set, table):
        """
            This method converts the SQLAlchemy query result set into a JSON array.
            :param result_set: Results from a SQLAlchemy query.
            :param result_set: SQLAlchemy ResultSet Object.
            :param table:  Table object that returned the results.
            :param table:  SQLAlchemy Table Object.
            :returns:  Jsonified SQLAlchemy ResultSet.
        """
        results = []
        if type(result_set) is list:
            col_types = dict()
            for result in result_set:
                table_json = {}
                for col in table._columns:
                    value = getattr(result, col.name)
                    if col.type in col_types.keys() and value is not None:
                        try:
                            table_json[col.name] = col_types[col.type](value)
                        except:
                            table_json[col.name] = "Error:  Failed to convert using ", str(col_types[col.type])
                    elif value is None:
                        table_json[col.name] = str()
                    else:
                        table_json[col.name] = value
                results.append(table_json)
            return results
        else:
            return self.to_json([result_set], table)