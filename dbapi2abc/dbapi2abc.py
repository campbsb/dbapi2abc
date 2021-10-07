# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Steve Campbell
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
=====
dbapi
=====

Implement abstract classes to present an interface to
PEP249 compliant database Connection and Cursor objects

See `PEP249
<https://www.python.org/dev/peps/pep-0249/>`_

"""
__author__ = "Steve Campbell"

from abc import ABC, abstractmethod
from typing import Optional, Sequence, Union

# NOTE: Don't abstract exceptions. Because the real exceptions won't inherit
# from them and hence will not be caught by except statements.

# Descriptions taken from https://www.python.org/dev/peps/pep-0249/

class Cursor(ABC):
    """
    These objects represent a database cursor, which is used to manage the
    context of a fetch operation. Cursors created from the same connection
    are not isolated, i.e., any changes done to the database by a cursor are
    immediately visible by the other cursors. Cursors created from different
    connections can or can not be isolated, depending on how the transaction
    support is implemented (see :meth:`Connection.rollback` and
    :meth:`Connection.commit`).
    """

    @property
    @abstractmethod
    def description(self) -> Optional[Sequence]:
        """
        This read-only attribute is a sequence of 7-item sequences.

        Each of these sequences contains information describing one result
        column:

        * name
        * type_code
        * display_size
        * internal_size
        * precision
        * scale
        * null_ok

        The first two items (name and type_code) are mandatory, the other five
        are optional and are set to None if no meaningful values can be
        provided.

        This attribute will be None for operations that do not return rows or
        if the cursor has not had an operation invoked via the
        :meth:`Cursor.execute`
        method yet.
        """
        pass

    @property
    @abstractmethod
    def rowcount(self) -> Optional[int]:
        """
        This read-only attribute specifies the number of rows that the last
        :meth:`Cursor.execute`
        produced (for DQL statements like SELECT) or affected (for
        DML statements like UPDATE or INSERT).

        NOTE: SQLite returns the number of rows the update where clause
        matches, not the number affected.

        The attribute is -1 in case no :meth:`Cursor.execute` has been
        performed on the cursor or the rowcount of the last operation is
        cannot be determined by the interface. Future versions of the DB API
        specification could redefine the latter case to have the object
        return None instead of -1.

        :return: The number of rows found or affected.
        """
        pass

    def callproc(self, procname: str, args: Union[list, tuple]):
        """
        Call a stored database procedure with the given name.
        The sequence of parameters must contain one entry for each argument
        that the procedure expects. The result of the call is returned as
        modified copy of the input sequence. Input parameters are left
        untouched, output and input / output parameters replaced with
        possibly new values.

        The procedure may also provide a result set as output. This must
        then be made available through the standard fetch() methods.

        This method is optional since not all databases provide stored
        procedures.

        :param procname: Name of the stored procedure to execute.
        :param args: Tuple or list of procedure parameters.
        :raise NotImplementedError: If called and it's not supported.
        :return: Modified copy of input sequence.
        """
        raise NotImplementedError(
            "The database engine does not support callproc!"
        )

    @abstractmethod
    def close(self) -> None:
        """
        Close the cursor now (rather than whenever __del__ is called).

        The cursor will be unusable from this point forward; an Error (or
        subclass) exception will be raised if any operation is attempted with
        the cursor.
        """
        pass

    @abstractmethod
    def execute(self, operation: str, parameters: Union[dict, list, tuple]):
        """
        Prepare and execute a database operation (query or command).

        Parameters may be provided as sequence or mapping and will be bound to
        variables in the operation. Variables are specified in a
        database-specific notation (see the module's paramstyle attribute for
        details)

        A reference to the operation will be retained by the cursor. If the
        same operation object is passed in again, then the cursor can optimize
        its behavior. This is most effective for algorithms where the same
        operation is used, but different parameters are bound to it (many
        times).

        For maximum efficiency when reusing an operation, it is best to use the
        .setinputsizes() method to specify the parameter types and sizes ahead
        of time. It is legal for a parameter to not match the predefined
        information; the implementation should compensate, possibly with a loss
        of efficiency.

        The parameters may also be specified as list of tuples to e.g. insert
        multiple rows in a single operation, but this kind of usage is
        deprecated:
        :meth:`~dbapi.Cursor.executemany`
        should be used instead.

        :param operation: The Query or command to be executed.
        :param parameters: The values to be bound into the operation.
        :return: The return type is not defined.
        """
        pass

    @abstractmethod
    def executemany(
            self, operation: str, parameters: Sequence[Union[dict, list, tuple]]
    ):
        """
        Prepare a database operation (query or command) and then execute it
        against all parameter sequences or mappings found in the sequence
        seq_of_parameters.

        Modules are free to implement this method using multiple calls to the
        .execute() method or by using array operations to have the database
        process the sequence as a whole in one call.

        Use of this method for an operation which produces one or more result
        sets constitutes undefined behavior, and the implementation is
        permitted (but not required) to raise an exception when it detects
        that a result set has been created by an invocation of the operation.

        The same comments as for :meth:`~dbapi.Cursor.execute` also apply
        accordingly to this method.

        :param operation: The Query or command to be executed.
        :param parameters: Sequence of sequence or mapping of bind values.
        :return: The return type is not defined.
        """
        pass

    @abstractmethod
    def fetchone(self) -> Optional[Sequence]:
        """
        Fetch the next row of a query result set, returning a single sequence,
        or None when no more data is available.

        An Error (or subclass) exception is raised if the previous call to
        :meth:`~dbapi.Cursor.execute` did not produce any result set or no call
        was issued yet.

        :raise Error:
        :return: Next row of data.
        """
        pass

    @abstractmethod
    def fetchmany(self, size: Optional[int] = None) -> Sequence[Sequence]:
        """
        Fetch the next set of rows of a query result, returning a sequence of
        sequences (e.g. a list of tuples). An empty sequence is returned when
        no more rows are available.

        The number of rows to fetch per call is specified by the parameter. If
        it is not given, the cursor's arraysize determines the number of rows
        to be fetched. The method should try to fetch as many rows as indicated
        by the size parameter. If this is not possible due to the specified
        number of rows not being available, fewer rows may be returned.

        An Error (or subclass) exception is raised if the previous call to
        :meth:`~dbapi.Cursor.execute` did not produce any result set or no call
        was issued yet.

        Note there are performance considerations involved with the size
        parameter. For optimal performance, it is usually best to use the
        .arraysize attribute. If the size parameter is used, then it is best
        for it to retain the same value from one .fetchmany() call to the next.

        :param size: Number of rows to fetch.
        :return: Sequence of rows of data.
        """
        pass

    @abstractmethod
    def fetchall(self) -> Sequence[Sequence]:
        """
        Fetch all (remaining) rows of a query result, returning them as a
        sequence of sequences (e.g. a list of tuples). Note that the
        cursor's arraysize attribute can affect the performance of this
        operation.

        An Error (or subclass) exception is raised if the previous call to
        :meth:`~dbapi.Cursor.execute` did not produce any result set or no call
        was issued yet.

        :return: Sequence of rows of data.
        """

    def nextset(self) -> Optional[bool]:
        """
        This method will make the cursor skip to the next available set,
        discarding any remaining rows from the current set.

        If there are no more sets, the method returns None. Otherwise,
        it returns a true value and subsequent calls to the
        :meth:`~dbapi.Cursor.fetch` methods will return rows from the next
        result set.

        This method is optional since not all databases support multiple result
        sets.

        An Error (or subclass) exception is raised if the previous call to
        :meth:`~dbapi.Cursor.execute` did not produce any result set or no call
        was issued yet.

        :raise NotImplementedError: If called and it's not supported.
        :return: True or None.
        """
        raise NotImplementedError(
            "The database engine does not support nextset!"
        )

    @property
    @abstractmethod
    def arraysize(self) -> int:
        """
        This read/write attribute specifies the number of rows to fetch at a
        time with
        :meth:`~dbapi.Cursor.fetchmany`
        It defaults to 1 meaning to fetch a single row at a time.

        Implementations must observe this value with respect to the
        :meth:`~dbapi.Cursor.fetchmany`
        method, but are free to interact with the database a single row at a
        time. It may also be used in the implementation of
        :meth:`~dbapi.Cursor.executemany`.

        :return: The number of rows to fetch.
        """
        pass

    @arraysize.setter
    @abstractmethod
    def arraysize(self, size: int):
        pass

    def setinputsizes(self, sizes: Sequence) -> None:
        """
        This can be used before a call to
        :meth:`~dbapi.Cursor.execute`
        to predefine memory areas for the operation's parameters.

        sizes is specified as a sequence — one item for each input parameter.
        The item should be a Type Object that corresponds to the input that
        will be used, or it should be an integer specifying the maximum
        length of a string parameter. If the item is None, then no predefined
        memory area will be reserved for that column (this is useful to avoid
        predefined areas for large inputs).

        This method would be used before the .execute*() method is invoked.

        Implementations are free to have this method do nothing and users are
        free to not use it.

        :param sizes: Sequence of Types or integer sizes1.
        """
        pass

    def setoutputsize(self, size: int, column: Optional[int] = None) -> None:
        """
        Set a column buffer size for fetches of large columns (e.g. LONGs,
        BLOBs, etc.). The column is specified as an index into the result
        sequence. Not specifying the column will set the default size for all
        large columns in the cursor.

        This method would be used before the
        :meth:`~dbapi.Cursor.execute`
        method is invoked.

        Implementations are free to have this method do nothing and users are
        free to not use it.

        :param size: Buffer size.
        :param column: Optional column index.
        """
        pass


class Connection(ABC):
    """ A Connection object represents an open database connection. """

    @abstractmethod
    def close(self) -> None:
        """
        Close the connection now (rather than whenever .__del__() is called).

        The connection will be unusable from this point forward; an Error
        (or subclass) exception will be raised if any operation is attempted
        with the connection. The same applies to all cursor objects trying to
        use the connection. Note that closing a connection without committing
        the changes first will cause an implicit rollback to be performed.
        :return: None.
        """
        pass

    @abstractmethod
    def commit(self) -> None:
        """
        Commit any pending transaction to the database.

        Note that if the database supports an auto-commit feature, this must
        be initially off. An interface method may be provided to turn it back
        on.

        Database modules that do not support transactions should implement this
        method with void functionality.
        :return: None.
        """
        pass

    def rollback(self) -> None:
        """
        This method is optional since not all databases provide transaction
        support.

        In case a database does provide transactions this method causes the
        database to roll back to the start of any pending transaction. Closing
        a connection without committing the changes first will cause an
        implicit rollback to be performed.
        :raise NotImplementedError: If called and it's not supported.
        :return: None.
        """
        raise NotImplementedError(
            "The database engine does not support rollback!"
        )

    @abstractmethod
    def cursor(self) -> Cursor:
        """
        Return a new Cursor Object using the connection.

        If the database does not provide a direct cursor concept, the module
        will have to emulate cursors using other means to the extent needed
        by this specification.
        :return: Database cursor.
        """
        pass
