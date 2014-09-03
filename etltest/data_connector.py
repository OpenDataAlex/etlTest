s__author__ = 'coty, ameadows'
"""
    This file contains all the logic to connect to data sources using SQLAlchemy.
"""

import logging
import sys

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
                                connection name from the connections settings file (default connections.cfg).
            :type conn_name: str
        """
        from etltest.utilities.settings_manager import SettingsManager

        self.log = logging.getLogger(name="DataConnector")
        self.log.setLevel(etltest_config['logging_level'])
        self.log.addHandler(console)

        self.conn_name = conn_name
        self.data_dir = SettingsManager().find_setting('Locations', 'data')

        connections = SettingsManager().get_connections()
        try:
            connection = connections[self.conn_name]
        except Exception:
            self.log.error("Connection %s does not exist, exiting." % conn_name)
            self.log.error(sys.exc_info()[0])
            raise

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

    def get_table(self, table_name, select_stmt=None):
        """
            This method gets a table from the data connection using SQLAlchemy's reflection capability. Columns in the
            select_stmt are included, with all other table columns excluded.
            :param table_name: The name of the table being reflected.
            :type table_name: str
            :param select_stmt: The fields being included in the query. Default None.
            :type select_stmt:  str
            :returns:  SQLAlchemy Table object
        """
        table = Table(table_name, self.meta)
        self.log.debug("Reflecting table %s" % table_name)

        if select_stmt == "all_columns":
            select_stmt = None

        self.insp.reflecttable(table, select_stmt)

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
        self.log.debug("Inserting records for table %s" % table_name)

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

    def select_data(self, select_stmt, from_stmt, where_stmt=None):
        #TODO:  How to handle complex WHERE clauses?
        #TODO:  Should we support sub-selects?
        #TODO:  Should we support joins?
        """
            This method queries records from the given table based on particular columns desired and the required
            filter criteria.  Currently only supports simple select queries.
            :param select_stmt:  Names of the columns to be returned from the query (SELECT clause).
            :param select_stmt: arr
            :param from_stmt:  Name of the table to be queried (FROM clause).
            :param from_stmt: str
            :param where_stmt:  The filter criteria for the query (WHERE clause)
            :param where_stmt:  arr
        """

        if select_stmt == "all_columns":
            table = self.get_table(from_stmt)
        else:
            table = self.get_table(from_stmt, select_stmt)

        if where_stmt is None:
            result = self.session.query(table)
        else:
            result = self.session.query(table).filter(where_stmt)

        self.log.debug(u"Executing query {0:s}".format(result))

        return self.to_json(result, table)

    def generate_data(self, table_name, records):
        """
        :param table_name: Name of the table yaml file that will be retrieved.
        :param table_name: str
        :param records: The set of keys for the records that need to be retrieved and inserted into the connection.
        :param records: arr
        :return: Formatted data set for the the data connector method.
        """

        full_set = YAMLParser().read_file(self.data_dir + "/" + self.conn_name + "/" + table_name + ".yml")
        subset = []
        for item in full_set:
            for record in records:
                try:
                    subset.append(item[record])
                except Exception:
                    self.log.info("Record %s is not in the full set." % record)
        return subset

    def to_json(self, result_set, table):
        """
            This method converts the SQLAlchemy query result set into a JSON array.
            :param result_set: Results from a SQLAlchemy query.
            :param result_set: SQLAlchemy ResultSet Object.
            :param table:  Table object that returned the results.
            :param table:  SQLAlchemy Table Object.
            :returns:  Jsonified SQLAlchemy ResultSet.
        """
        results = [] # In the event nothing is in the set, return empty set.
        col_types = dict()
        for result in result_set:
            self.log.debug(u"Processing record: {0:s}".format(result))
            table_json = {}
            i = 0
            for column in table._columns:
                value = result[i]
                if value is None:
                    table_json[column.name] = str()
                else:
                    table_json[column.name] = value
                i += 1
            results.append(table_json)

        return results