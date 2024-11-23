"""Package for the remoteset distribution."""

import os

import Ice

try:
    import RemoteTypes  # noqa: F401

except ImportError:
    slice_path = os.path.join(
        os.path.dirname(__file__),
        "remotetypes.ice",
    )

    Ice.loadSlice(slice_path)
    import RemoteTypes  # noqa: F401
