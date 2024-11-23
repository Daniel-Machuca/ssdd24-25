"""Needed classes for implementing the Iterable interface for different types of objects."""

import RemoteTypes as rt  # noqa: F401; pylint: disable=import-error

# TODO: It's very likely that the same Iterable implementation doesn't fit
# for the 3 needed types. It is valid to implement 3 different classes implementing
# the same interface and use an object from different implementations when needed.


class Iterable(rt.Iterable):
    """Skeleton for an Iterable implementation."""
