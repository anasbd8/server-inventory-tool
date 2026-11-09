"""Entry point for the server inventory tool."""

import os
from pathlib import Path

from menu import run_menu
from storage import load_servers


def main():
    """Load the server data and start the text menu."""
    # The default path is relative to the directory where the program is run.
    data_file = Path(os.getenv("INVENTORY_DATAFILE", "servers.json"))
    servers = load_servers(data_file)
    run_menu(servers, data_file)

if __name__ == "__main__":
    main()
