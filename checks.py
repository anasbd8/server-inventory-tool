"""Functions for checking whether servers respond to ping."""

# subprocess lets Python run external programs such as ping.
import subprocess
from datetime import datetime

from storage import save_servers


def ping_server(address):
    """Return True if the address responds, otherwise False (Linux/macOS).

    The caller must handle errors if ping cannot be started.
    """
    try:
        # Pass the command as a list: -c 1 sends one ping packet.
        # capture_output captures output so it does not interrupt the menu.
        # timeout stops the process if it takes more than five seconds.
        result = subprocess.run(
            ["ping", "-c", "1", address],
            capture_output=True,
            timeout=5,
        )
    except subprocess.TimeoutExpired:
        # Treat a check that exceeds the time limit as down.
        return False

    # Exit code 0 means ping succeeded. Other codes produce False.
    return result.returncode == 0


def check_server(server, servers, data_file):
    """Check a server, save the entire list and return whether it responded."""
    # Run ping before changing the server. If ping cannot start, an error is
    # raised before the server data is modified.
    is_up = ping_server(server["address"])

    # Update the same dictionary that is stored in the server list.
    if is_up:
        server["status"] = "up"
    else:
        server["status"] = "down"

    # Store the local time as text, for example 2026-11-10 21:30.
    server["last_checked"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Save the entire list so the result persists after restarting.
    save_servers(servers, data_file)
    return is_up


def check_all_servers(servers, data_file):
    """Check all servers and save the results."""
    # Check one server at a time. check_server saves the list after each check.
    for server in servers:
        check_server(server, servers, data_file)
