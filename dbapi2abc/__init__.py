"""
dbapi2abc
==========

This package provides abstract classes to present an interface to
PEP249 compliant database Connection and Cursor objects.

This allows you to use type hints on functions handling database
connections and cursors without needing to specify the specific
backend database engine being used.

``
from dbapi2abc import Connection, Cursor

class MyObject():
    def __init__(self, db: Connection):
        self.db = db

    def run_some_query(self) -> Cursor:
        cur = self.db.cursor()
        cur.execute("SELECT * FROM Table")
        return cur
``
"""

from .dbapi2abc import Connection, Cursor
