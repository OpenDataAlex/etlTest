__author__ = 'ameadows'
from unittest import TestCase, main
import sqlalchemy

def set_up(self):
    engine = sqlalchemy.create_engine()