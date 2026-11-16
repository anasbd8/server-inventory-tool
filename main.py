"""Entry point for the server inventory tool."""

import os
import sys
from pathlib import Path
import argparse

from menu import run_menu, display_servers
from storage import load_servers, export_servers
from checks import check_server, check_all_servers


def main():
    """Parse command-line flags, load the server data and run the chosen action.

    Without any action flag, the interactive text menu is started.
    """
    # Create a parser for command-line arguments.
    parser = argparse.ArgumentParser(description="Manage a simple server inventory.")
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all servers and exit without opening the menu",
    )

    parser.add_argument(
        "--environment",
        choices=["dev", "test", "prod"],
        help="Filter servers by environment",
    )

    parser.add_argument(
        "--check",
        help="Check a server by name",
    )

    parser.add_argument(
        "--check-all",
        action="store_true",
        help="Check all servers"
    )

    # Register the CSV export flag.
    parser.add_argument(
        "--export",
        action="store_true",
        help="Export all servers to CSV",
    )
    # Read the arguments supplied in the terminal.
    args = parser.parse_args()

    # The default path is relative to the directory where the program is run.
    data_file = Path(os.getenv("INVENTORY_DATAFILE", "servers.json"))
    servers = load_servers(data_file)

    if args.list:
        filtered_servers = servers
        # Keep only servers that match the requested environment.
        if args.environment:
            filtered_servers = []
            for server in servers:
                if server["environment"] == args.environment:
                    filtered_servers.append(server)
        display_servers(filtered_servers)
    elif args.check:
        # Store the matching server, or None if no match is found.
        selected_server = None
        for server in servers:
            if server["name"].casefold() == args.check.casefold():
                selected_server = server
                break
        # Inform the user when the requested server does not exist.
        if selected_server is None:
            print(f"Did not find {args.check}")
            # Exit with an error code when the server does not exist.
            sys.exit(1)
        else:
            # Check the server and save its status and timestamp.
            is_up = check_server(selected_server, servers, data_file)
            # Display the updated status.
            print(f"Server {selected_server['name']}: {selected_server['status']}")
            # Return an exit code based on the ping result.
            if is_up:
                sys.exit(0)
            else:
                sys.exit(1)
    elif args.check_all:
        # Check all servers, save the results and display their statuses.
        check_all_servers(servers, data_file)
        display_servers(servers)
        # Track whether at least one checked server is down.
        has_down = False
        for server in servers:
            if server["status"] == "down":
                has_down = True
        if has_down:
            # Exit with an error code if any server is down.
            sys.exit(1)
        else:
            sys.exit(0)
    elif args.export:
        # Export all servers and store the report path.
        report_file = export_servers(servers)
        # Display where the report was saved.
        print(f"Report saved to: {report_file}")
        sys.exit(0)
    else:
        run_menu(servers, data_file)


if __name__ == "__main__":
    main()
