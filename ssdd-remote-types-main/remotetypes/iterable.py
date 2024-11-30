"""Needed classes for implementing the Iterable interface for different types of objects."""
from typing import Optional
import Ice
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error

# TODO: It's very likely that the same Iterable implementation doesn't fit
# for the 3 needed types. It is valid to implement 3 different classes implementing
# the same interface and use an object from different implementations when needed.


class DictIterable(rt.Iterable):
    """Implementation of the iterable interface for dictionaries."""

    def __init__(self, data: dict, current_hash: int) -> None:
        """Initialize a DictIterable."""
        self._data = iter(data.keys())
        self._original_hash = current_hash
        self._modified = False

    def mark_as_modified(self) -> None:
        """Mark the iterator as invalid if the dictionary is modified."""
        self._modified = True

    def next(self, current: Optional[Ice.Current] = None) -> str:
        """Retrieve the next key in the iteration."""
        if self._modified:
            raise rt.CancelIteration()
        try:
            return next(self._data)
        except StopIteration as exc:
            raise rt.StopIteration() from exc


class ListIterable(rt.Iterable):
    """Implementation of the iterable interfaace for lists"""

    def __init__(self, data: list, current_hash: int) -> None:
        """Initialize a ListIterable."""
        self._data = iter(data)
        self._original_hash = current_hash
        self._modified = False

    def mark_as_modified(self) -> None:
        """Mark the iterator as invalid if the list is modified."""
        self._modified = True

    def next(self, current: Optional[Ice.Current] = None) -> str:
        """Retrieve the next element in the iteration."""
        if self._modified:
            raise rt.CancelIteration()
        try:
            return next(self._data)
        except StopIteration as exc:
            raise rt.StopIteration() from exc


class SetIterable(rt.Iterable):
    """Implementation of the iterable interface for sets"""
    def __init__(self, data: set, current_hash: int) -> None:
        """Initialize a SetIterable."""
        self._data = iter(data)
        self._original_hash = current_hash
        self._modified = False

    def mark_as_modified(self) -> None:
        """Mark the iterator as invalid if the set is modified."""
        self._modified = True

    def next(self, current: Optional[Ice.Current] = None) -> str:
        """Retrieve the next element in the iteration."""
        if self._modified:
            raise rt.CancelIteration()
        try:
            return next(self._data)
        except StopIteration as exc:
            raise rt.StopIteration() from exc
