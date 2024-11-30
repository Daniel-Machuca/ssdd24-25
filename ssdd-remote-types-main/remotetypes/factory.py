"""Needed classes to implement the Factory interface."""

from typing import Dict, Optional
import Ice
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
from remotetypes.remotedict import RemoteDict
from remotetypes.remotelist import RemoteList
from remotetypes.remoteset import RemoteSet

# pylint: disable=too-few-public-methods
class Factory(rt.Factory):
    """Skeleton for the Factory implementation."""

    def __init__(self) -> None:
        self._registry: Dict[str, Ice.Identity] = {}

    def get(
        self,
        type_name: rt.TypeName,
        identifier: Optional[str] = None,
        current: Optional[Ice.Current] = None,
    ) -> rt.RType:
        """retrieve an exixting object or create a new one, allowing the
        creation of objects RDict, RList or RSet"""
        print(f"get called with type_name={type_name}, identifier={identifier}")

        if identifier is None:
            identifier = f"{type_name}_{len(self._registry)}"

        if identifier in self._registry:
            print(f"Returning existing proxy for identifier={identifier}")
            proxy = current.adapter.createProxy(self._registry[identifier])
            return rt.RTypePrx.uncheckedCast(proxy)

        print(f"Creating new object of type {type_name}")
        if type_name == rt.type_name.RDict:
            obj = RemoteDict(identifier, storage_file=f"{identifier}.json")
        elif type_name == rt.type_name.RList:
            obj = RemoteList(identifier, storage_file=f"{identifier}.json")
        elif type_name == rt.type_name.RSet:
            obj = RemoteSet(identifier)
        else:
            raise rt.TypeError(f"Unknown type_name: {type_name}")

        identity = Ice.Identity(name=identifier)
        current.adapter.add(obj, identity)
        self._registry[identifier] = identity

        proxy = current.adapter.createProxy(identity)
        print(f"Object created and proxy returned: {proxy}")
        return rt.RTypePrx.uncheckedCast(proxy)
