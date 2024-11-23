"""Needed classes to implement and serve the RDict type."""

import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
from typing import Optional, Dict
from remotetypes.iterable import DictIterable
import hashlib
import os
import json
import Ice


class RemoteDict(rt.RDict):
    """Skeleton for the RDict implementation."""
    def __init__(self, identifier: str, storage_file: Optional[str] = None) -> None:
        self.identifier = identifier
        self.storage: Dict[str, str] = {}
        self.storage_file = storage_file
        if self.storage_file:
            self._load_from_file()
            
    def identifier(self, current: Optional[Ice.Current] = None) -> str:
        """Return the identifier of the object."""
        return self.identifier
    '''--------------------------------------------------------RDict needed methods--------------------------------------------------------------'''
    
    def setItem(self, key: str, item: str, current: Optional[Ice.Current] = None) -> None:
        """Set a value for a given key in the dictionary."""
        self.storage[key] = item
        self._persist_to_file()
        
    def getItem(self, key: str, current: Optional[Ice.Current] = None) -> str:
        """Retrieve the value for a given key."""
        if key not in self.storage:
            raise rt.KeyError(key)
        return self.storage[key]
    
    def pop(self, key: str, current: Optional[Ice.Current] = None) -> str:
        """Remove and return the value associated with a given key."""
        if key not in self.storage:
            raise rt.KeyError(key)
        value = self.storage.pop(key)
        self._persist_to_file()
        return value
    
    '''-------------------------------------------------------persistence----------------------------------------------------------------------'''
    
    def _persist_to_file(self) -> None:
        """Persist the current state to a JSON file."""
        if self.storage_file:
            try:
                with open(self.storage_file, "w", encoding="utf-8") as file:
                    json.dump(self.storage, file, indent=4)
            except Exception as e:
                print(f"Error persisting to file {self.storage_file}: {e}")

    def _load_from_file(self) -> None:
        """Load the state from a JSON file if it exists, or create an empty file."""
        if self.storage_file:
            # Crea el archivo vacío si no existe
            if not os.path.exists(self.storage_file):
                print(f"Archivo {self.storage_file} no existe. Creándolo...")
                with open(self.storage_file, "w", encoding="utf-8") as file:
                    json.dump({}, file)
            try:
                with open(self.storage_file, "r", encoding="utf-8") as file:
                    self.storage = json.load(file)
            except json.JSONDecodeError:
                print(f"Archivo {self.storage_file} corrupto. Reiniciando...")
                self.storage = {}


            
    '''-------------------------------------------------------------------------------------------------------------------------------------------'''
    
    def remove(self, item: str, current: Optional[Ice.Current] = None) -> None:
        """Remove an item (key) from the dictionary."""
        if item not in self.storage:
            raise rt.KeyError(item)
        del self.storage[item]
        self._persist_to_file()
        
    def length(self, current: Optional[Ice.Current] = None) -> int:
        """Return the number of elements in the dictionary."""
        return len(self.storage)

    def contains(self, item: str, current: Optional[Ice.Current] = None) -> bool:
        """Check if a key exists in the dictionary."""
        return item in self.storage
    
    def hash(self, current: Optional[Ice.Current] = None) -> int:
        """Calculate a hash based on the dictionary's content."""
        contents = list(self.storage.items())
        contents.sort()  
        return hash(repr(contents))
    
    def iter(self, current: Optional[Ice.Current] = None) -> rt.IterablePrx:
        """Create an iterable object."""
        current_hash = self.hash()
        iterable = DictIterable(self.storage, current_hash)

        proxy = current.adapter.addWithUUID(iterable)
        return rt.IterablePrx.uncheckedCast(proxy)


    
