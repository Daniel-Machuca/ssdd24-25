"""Needed classes to implement and serve the RList type."""

import os
import json
from typing import Optional, List
import Ice
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
from remotetypes.iterable import ListIterable


# pylint: disable=too-few-public-methods
class RemoteList(rt.RList):
    """Skelenton for the RList implementation."""

    def __init__(self, identifier: str, storage_file: Optional[str] = None) -> None:
        self._identifier = identifier
        self.storage: List[str] = []
        self.storage_file = storage_file
        if self.storage_file:
            self._load_from_file()

    def identifier(self) -> str:
        """Return the identifier of the object."""
        return self._identifier

    def append(self, item: str) -> None:
        """Add an item to the end of the list."""
        self.storage.append(item)
        self._persist_to_file()

    def pop(self, index: Optional[int] = None) -> str:
        """
        Remove and return an item at the specified index.
        If no index is specified, remove and return the last item.
        """
        try:
            if index is None:
                return self.storage.pop()
            return self.storage.pop(index)
        except IndexError as error:
            raise rt.IndexError(f"Index {index} is out of range.") from error
        finally:
            self._persist_to_file()

    # pylint: disable=invalid-name
    def getItem(self, index: int) -> str:
        """Retrieve an item at the specified index."""
        try:
            return self.storage[index]
        except IndexError as error:
            raise rt.IndexError(f"Index {index} is out of range.") from error

    def _persist_to_file(self) -> None:
        """Persist the current state to a JSON file."""
        if self.storage_file:
            try:
                with open(self.storage_file, "w", encoding="utf-8") as file:
                    json.dump(self.storage, file, indent=4)
            except Exception as exception:
                print(f"Error persisting to file {self.storage_file}: {exception}")

    def _load_from_file(self) -> None:
        """Load the state from a JSON file if it exists."""
        try:
            if self.storage_file and not os.path.exists(self.storage_file):
                with open(self.storage_file, "w", encoding="utf-8") as file:
                    json.dump([], file, indent=4)
            with open(self.storage_file, "r", encoding="utf-8") as file:
                self.storage = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.storage = []

    def remove(self, item: str) -> None:
        """Remove an item from the list."""
        try:
            self.storage.remove(item)
        except ValueError as error:
            raise rt.KeyError(item) from error
        self._persist_to_file()

    def length(self) -> int:
        """Return the number of elements in the list."""
        return len(self.storage)

    def contains(self, item: str) -> bool:
        """Check if an item exists in the list."""
        return item in self.storage

    def hash(self) -> int:
        """Calculate a hash based on the list's content."""
        return hash(repr(self.storage))

    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """Create an iterable object."""
        current_hash = self.hash()
        iterable = ListIterable(self.storage, current_hash)

        proxy = current.adapter.addWithUUID(iterable)
        return rt.IterablePrx.uncheckedCast(proxy)
