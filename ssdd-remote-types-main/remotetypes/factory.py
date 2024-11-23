"""Needed classes to implement the Factory interface."""

import Ice
import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error
from typing import Dict, Optional
from remotetypes.remotedict import RemoteDict
from remotetypes.remotelist import RemoteList
from remotetypes.remoteset import RemoteSet


class Factory(rt.Factory):
    """Skeleton for the Factory implementation."""
    
    def __init__(self) -> None:
        self._registry: Dict[str, Ice.Identity] = {} 
        
    def get(self, typeName: rt.TypeName, identifier: Optional[str] = None, current: Optional[Ice.Current] = None) -> rt.RType:
        print(f"get called with typeName={typeName}, identifier={identifier}")

        if identifier is None:
            identifier = f"{typeName}_{len(self._registry)}"

        if identifier in self._registry:
            print(f"Returning existing proxy for identifier={identifier}")
            proxy = current.adapter.createProxy(self._registry[identifier])
            return rt.RTypePrx.uncheckedCast(proxy)

        print(f"Creating new object of type {typeName}")
        if typeName == rt.TypeName.RDict:
            obj = RemoteDict(identifier, storage_file=f"{identifier}.json")
        elif typeName == rt.TypeName.RList:
            obj = RemoteList(identifier, storage_file=f"{identifier}.json")
        elif typeName == rt.TypeName.RSet:
            obj = RemoteSet(identifier)
        else:
            raise rt.TypeError(f"Unknown TypeName: {typeName}")

        identity = Ice.Identity(name=identifier)
        current.adapter.add(obj, identity)  
        self._registry[identifier] = identity  

        proxy = current.adapter.createProxy(identity)  
        print(f"Object created and proxy returned: {proxy}")
        return rt.RTypePrx.uncheckedCast(proxy)
