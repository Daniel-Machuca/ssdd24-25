"""Module containing the handler functions for CLI commands."""

import logging
import os
import sys

from remotetypes.server import Server


def remotetypes_server() -> None:
    """Handle for running the server for remote types."""
    logging.basicConfig(level=logging.DEBUG)

    cmd_name = os.path.basename(sys.argv[0])

    logger = logging.getLogger(cmd_name)
    logger.info("Running remotetypes server...")

    server = Server()
    sys.exit(server.main(sys.argv))
