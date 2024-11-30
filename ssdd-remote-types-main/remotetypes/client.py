"""Client for testing the remotetypes server."""

import sys
import os
import json
import Ice
from remotetypes.factory import Factory
import RemoteTypes


def main():
    """Main client logic."""
    with Ice.initialize(sys.argv) as communicator:
        proxy = communicator.stringToProxy("factory:tcp -h localhost -p 10000")

        factory = RemoteTypes.FactoryPrx.checkedCast(proxy)

        if not factory:
            raise RuntimeError("Invalid proxy. Could not connect to the server.")

        print("Connected to the server.")

        print("Creating a new RemoteSet...")
        rset = factory.get(RemoteTypes.TypeName.RSet, "test_set")
        rset = RemoteTypes.RSetPrx.checkedCast(rset)
        if not rset:
            raise RuntimeError("Invalid proxy for RSet")

        rset.add("item1")
        rset.add("item2")
        print(f"Set contains 'item1': {rset.contains('item1')}")
        print(f"Set length: {rset.length()}")

        print("Iterating over the set:")
        iterator = rset.iter()
        try:
            while True:
                print(f"Item: {iterator.next()}")
        except RemoteTypes.StopIteration:
            print("Finished iterating.")

        print("Creating a new RemoteDict...")
        rdict = RemoteTypes.RDictPrx.checkedCast(
            factory.get(RemoteTypes.TypeName.RDict, "test_dict")
        )
        if not rdict:
            raise RuntimeError("Invalid proxy for RemoteDict.")
        rdict.setItem("key1", "value1")
        print(f"Value for 'key1': {rdict.getItem('key1')}")
        print(f"Dict length: {rdict.length()}")
        rdict = RemoteTypes.RDictPrx.checkedCast(
            factory.get(RemoteTypes.TypeName.RDict, "test_dict")
        )

        rdict.setItem("pruebajson", "pruebas")
        json_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "test_dict.json")
        )

        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            assert (
                data["key1"] == "value1"
            ), "Persistencia fallida: No se guardó correctamente el valor en el JSON."
        print(
            "Persistencia verificada: El fichero JSON contiene los datos correctamente."
        )

        print("Creating a new RemoteList...")
        rlist = RemoteTypes.RListPrx.checkedCast(
            factory.get(RemoteTypes.TypeName.RList, "test_list")
        )
        if not rlist:
            raise RuntimeError("Invalid proxy for RemoteList.")
        rlist.append("item1")
        rlist.append("item2")
        print(f"List contains 'item1': {rlist.contains('item1')}")
        print(f"List length: {rlist.length()}")

        print("Iterating over the list:")
        iterator = rlist.iter()
        try:
            while True:
                print(f"Item: {iterator.next()}")
        except RemoteTypes.StopIteration:
            print("Finished iterating.")

        print("Client finished successfully.")


if __name__ == "__main__":
    main()
