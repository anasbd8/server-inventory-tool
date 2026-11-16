"""Functions for JSON storage and CSV reports."""

# Standard library tools for CSV, JSON, timestamps and file paths.
import csv
import json
from datetime import datetime
from pathlib import Path


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
        # indent=4 adds line breaks and indentation so the file is easy to read.
        json.dump(servers, file, indent=4)


def export_servers(servers):
    """Export all servers to a CSV report and return its path."""
    reports = Path("reports")
    # Create the directory. exist_ok=True allows it to already exist.
    reports.mkdir(exist_ok=True)

    # Format the current local time, for example 2026-11-12_1430.
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")

    # Build the CSV file path inside the reports directory.
    report_file = reports / f"inventory_{timestamp}.csv"

    # Set the column names and their order to match the dictionary keys.
    fieldnames = [
        "name", "address", "environment",
        "role", "status", "last_checked"
    ]

    # Open the file for writing. with closes it automatically.
    # newline="" lets csv handle line endings; UTF-8 supports non-ASCII text.
    with open(report_file, "w", newline="", encoding="utf-8") as file:
        # Map each dictionary key to its column.
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the column headers on the first row.
        writer.writeheader()

        # Write one row for each server in the list.
        writer.writerows(servers)

    # Return the path so the caller can show where the report was saved.
    return report_file
