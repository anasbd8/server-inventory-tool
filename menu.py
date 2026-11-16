"""Text menu and server display functions."""

# Import the storage and check functions that the menu uses.
from storage import save_servers, export_servers
from checks import check_server, check_all_servers

def display_servers(servers):
    """Display server names, environments and statuses in aligned columns."""
    # < aligns text to the left. The numbers set the minimum column widths.
    print(f"{'Name':<15}{'Environment':<15}{'Status':<10}")
    # Go through the list and print one row for each server.
    for server in servers:
        # Use the keys to get values from the server dictionary.
        print(f"{server['name']:<15}{server['environment']:<15}{server['status']:<10}")


def add_server(servers, data_file):
    """Add a new server to the list and save it."""
    name = input("Enter server name: ").strip()

    # Check whether another server already uses this name.
    for server in servers:
        # Compare names without distinguishing uppercase and lowercase letters.
        if server["name"].casefold() == name.casefold():
            print(f"A server named {name} already exists.")
            return

    address = input("Enter server address: ").strip()

    # Keep asking until the user enters a valid environment.
    while True:
        environment = input("Enter environment (dev/test/prod): ").strip()

        if environment in ("dev", "test", "prod"):
            break

        print("Invalid environment. Choose dev, test or prod.")

    role = input("Enter server role: ").strip()
    # Create a dictionary for the new server.
    new_server = {
        "name": name,
        "address": address,
        "environment": environment,
        "status": "unknown",
        "role": role,
        "last_checked": ""
    }
    # Add the new server to the list.
    servers.append(new_server)
    # Save the updated server list.
    save_servers(servers, data_file)
    print(f"Server {name} added successfully.")


def remove_server(servers, data_file):
    """Remove a server and save the updated list."""
    name = input("Enter server name to remove: ").strip()

    for server in servers:
        if server["name"].casefold() == name.casefold():
            # Production servers require extra confirmation.
            if server["environment"] == "prod":
                confirmation = input(
                    "This is a production server. Remove it? (yes/no): "
                ).strip().casefold()

                if confirmation != "yes":
                    print("Removal cancelled.")
                    return

            # Remove the matching server and save the change.
            servers.remove(server)
            save_servers(servers, data_file)
            print(f"Server {server['name']} removed successfully.")
            return

    print(f"No server named {name} was found.")


def display_servers_by_environment(servers):
    """Display only servers in the selected environment."""
    while True:
        environment = input("Enter environment to filter by (dev/test/prod): ").strip()

        if environment in ("dev", "test", "prod"):
            break

        print("Invalid environment. Choose dev, test or prod.")

    # Collect the servers that belong to the selected environment.
    filtered_servers = []
    for server in servers:
        if server["environment"] == environment:
            filtered_servers.append(server)

    # Reuse the existing table display function.
    display_servers(filtered_servers)


def check_server_by_name(servers, data_file):
    """Ask for a server name and display the check result."""
    name = input("Enter server name to check: ").strip()

    # Find the server name without distinguishing uppercase and lowercase.
    for server in servers:
        if server["name"].casefold() == name.casefold():
            try:
                # The check function updates the status, timestamp and JSON file.
                check_server(server, servers, data_file)
            except OSError as error:
                # Report an error if ping cannot run or the result cannot be saved.
                print(f"Could not complete or save the check: {error}")
                return

            print(f"{server['name']}: {server['status']} ({server['last_checked']})")
            return

    # If the loop found no match, the name is not in the list.
    print(f"No server named {name} was found.")


def run_menu(servers, data_file):
    """Repeat the menu until the user chooses to exit."""
    # The loop continues until break stops it.
    while True:
        print("\nServer inventory")
        print("1. List all servers")
        print("2. Add a new server ")
        print("3. Remove a server ")
        print("4. Check a server ")
        print("5. Check all servers ")
        print("6. Export the server list to CSV ")
        print("7. List servers by environment")
        print("0. Exit")
        # input returns a string. strip removes leading and trailing whitespace.
        choice = input("Choose an option: ").strip()

        # Compare with strings such as "1" because the user's input is text.
        if choice == "1":
            # Pass the server list to the function that displays the table.
            display_servers(servers)
        elif choice == "2":
            add_server(servers, data_file)
        elif choice == "3":
            remove_server(servers, data_file)
        elif choice == "4":
            # Check a named server and then return to the menu.
            check_server_by_name(servers, data_file)
        elif choice == "5":
            # Check all servers and display their updated statuses.
            check_all_servers(servers, data_file)
            display_servers(servers)
        elif choice == "6":
            # Run the export and store the returned file path.
            report_file = export_servers(servers)
            # Display where the report was saved.
            print(f"Report saved to: {report_file}")
        elif choice == "7":
            display_servers_by_environment(servers)
        elif choice == "0":
            # Stop the menu loop and leave the function.
            break
        else:
            # After the error message, the loop displays the menu again.
            print("Invalid choice. Please try again.")
