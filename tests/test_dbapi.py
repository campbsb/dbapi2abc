# Test using 'pytest'
import dbapi
from typing import List, Optional, Sequence


class TestConnection(dbapi.Connection):
    def close(self) -> None:
        pass

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    def cursor(self) -> dbapi.Cursor:
        pass


class TestCursor(dbapi.Cursor):

    def arraysize(self) -> int:
        pass

    def description(self) -> Optional[Sequence]:
        pass

    def rowcount(self) -> Optional[int]:
        pass

    def close(self) -> None:
        pass

    def execute(self, operation: str, parameters: list):
        pass

    def executemany(self, operation: str, parameters: List[list]):
        pass

    def fetchall(self) -> Sequence[Sequence]:
        pass

    def fetchmany(self, size: Optional[int] = None) -> Sequence[Sequence]:
        pass

    def fetchone(self) -> Optional[Sequence]:
        pass


def test_connection():
    db = TestConnection()
    assert isinstance(db, dbapi.Connection)


def test_cursor():
    db = TestCursor()
    assert isinstance(db, dbapi.Cursor)
