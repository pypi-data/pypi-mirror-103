"""
Core functionality implemented by pyduckdb.

This is mostly the concrete implementation of the DB 2.0 API.

"""
# pylint: disable=import-error
from pyduckdb.core.exceptions import (
    DatabaseError,
    DataError,
    Error,
    InterfaceError,
    IntegrityError,
    InternalError,
    NotSupportedError,
    OperationalError,
    ProgrammingError,
)
from .connection import AsyncConnection
from .cursor import AsyncCursor

__all__ = [
    "AsyncConnection",
    "AsyncCursor",
    "Error",
    "InterfaceError",
    "DatabaseError",
    "DataError",
    "IntegrityError",
    "InternalError",
    "NotSupportedError",
    "OperationalError",
    "ProgrammingError",
]
