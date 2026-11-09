"""Functions for loading and saving server data as JSON."""

import json


def load_servers(data_file):
    """Load the server list, or return an empty list if the file is missing."""
    # Check whether the JSON file exists before trying to open it.
    if data_file.exists():
        # Open the file for reading. with closes it when the block ends.
        with open(data_file, "r") as file:
            # Convert JSON into Python objects: a list of server dictionaries.
            # Example fields: {"name": "web01", "environment": "prod", "status": "unknown"}
            servers = json.load(file)
    else:
        # An empty list lets the program start even when the file is missing.
        servers = []
    return servers


def save_servers(servers, data_file):
    """Save the server list to the selected JSON file."""
    # Opening with "w" replaces the previous file contents.
    with open(data_file, "w") as file:
        json.dump(servers, file)
