// -*- mode: c++ -*-

module RemoteTypes {
    exception KeyError { string key; };
    exception IndexError { string message; };
    exception TypeError { string description; };
    exception StopIteration {};
    exception CancelIteration {};

    enum TypeName { RDict, RList, RSet };

    interface Iterable {
        string next() throws StopIteration, CancelIteration;
    };

    interface RType {
        idempotent string identifier();
        void remove(string item) throws KeyError;
        idempotent int length();
        idempotent bool contains(string item);
        idempotent long hash();
        Iterable* iter();
    };

    interface RDict extends RType {
        idempotent void setItem(string key, string item);
        idempotent string getItem(string key) throws KeyError;
        string pop(string key) throws KeyError;
    };

    interface RList extends RType {
        void append(string item);
        string pop(optional(1) int index) throws IndexError;
        idempotent string getItem(int index) throws IndexError;
    };

    interface RSet extends RType {
        idempotent void add(string item);
        string pop() throws KeyError;
    };

    interface Factory {
        RType* get(TypeName typeName, optional(1) string identifier);
    };
}
