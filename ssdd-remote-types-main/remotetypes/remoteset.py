"""Needed classes to implement and serve the RSet type."""

from typing import Optional
import Ice
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
from remotetypes.customset import StringSet
from remotetypes.iterable import SetIterable


class RemoteSet(rt.RSet):
    """Implementation of the remote interface RSet."""

    def __init__(self, identifier) -> None:
        print(f"Initializing RemoteSet with identifier: {identifier}")
        self.identifier = identifier
        self.storage = set()

    def identifier(self, current: Optional[Ice.Current] = None) -> str:
        """Return the identifier of the object."""
        return self.identifier

    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Remove an item from the StringSet if added. Else, raise a remote exception."""
        try:
            self.storage.remove(item)
        except KeyError as error:
            raise rt.KeyError(item) from error

    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the number of elements in the StringSet."""
        return len(self.storage)

    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        """Check the pertenence of an item to the StringSet."""
        return item in self.storage

    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Calculate a hash from the content of the internal StringSet."""
        contents = list(self.storage)
        contents.sort()
        return hash(repr(contents))

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """Create an iterable object."""
        current_hash = hash(frozenset(self.storage))
        iterable = SetIterable(self.storage, current_hash)

        proxy = current.adapter.addWithUUID(iterable)
        return rt.IterablePrx.uncheckedCast(proxy)

    def add(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Add a new string to the StringSet."""
        self.storage.add(item)

    def pop(self, current: Optional[Ice.Current] = None) -> str:
        """Remove and return an element from the storage."""
        try:
            return self.storage.pop()

        except KeyError as exc:
            raise rt.KeyError() from exc
