# Server Inventory Tool

Server Inventory Tool is a Python program for managing a small server inventory. It stores each server's name, address, environment, role, status and latest check time in a JSON file.

The program supports both an interactive text menu and command-line arguments. Both interfaces reuse the same storage, ping and CSV export functions.

## Features

- List all servers or filter them by environment.
- Add servers with environment validation and duplicate-name checks.
- Remove servers, with extra confirmation for production servers.
- Check one server or all servers using ping.
- Save changes, including check results and timestamps, to JSON.
- Export all servers to a timestamped CSV report.
- Return exit codes that can be used in shell scripts.

## Requirements

- Python 3.
- Linux or macOS with the `ping` command available. Windows users can run the program in WSL or a Linux course environment.
- Permission to read and write the selected data file and create the report directory.

There are no external Python dependencies to install. The program uses only the standard library: `argparse`, `os`, `sys`, `pathlib`, `json`, `csv`, `datetime` and `subprocess`.

The ping command uses `-c 1`, which sends one packet on Linux/macOS. These flags are not intended for native Windows ping.

## Getting started

Clone or download the repository and open a terminal in its root directory, where `main.py` and `servers.json` are located.

```bash
# Check Python and display the available arguments.
python3 --version
python3 main.py --help

# Start the interactive menu.
python3 main.py
```

No virtual environment or package installation is required. If your Python 3 interpreter is called `python` instead of `python3`, use that command instead.

Run the commands from the project directory. The default data file and report directory are relative to the current working directory.

## Interactive menu

Start the menu with:

```bash
python3 main.py
```

| Option | Action |
| --- | --- |
| `1` | Display all servers. |
| `2` | Add a server: enter its name, address, environment and role. |
| `3` | Remove a server by name. Production servers require confirmation with `yes`. |
| `4` | Check one server by name and display its status and check time. |
| `5` | Check all servers and display the updated table. |
| `6` | Export all servers to CSV and display the report path. |
| `7` | Display servers in a selected environment. |
| `0` | Exit. |

The menu repeats after an operation or an invalid menu choice. When adding or filtering servers, an invalid environment produces a message and another prompt. The accepted environments are `dev`, `test` and `prod`.

Server names are matched case-insensitively when checking for duplicates, removing a server or checking a server. For example, `WEB01` matches `web01`. Newly added servers have status `unknown` and an empty check timestamp. Removing a production server is cancelled unless the confirmation is `yes`, ignoring case and surrounding whitespace.

Server tables use aligned columns. Example output before any checks:

```text
Name           Environment    Status
web01          prod           unknown
db01           prod           unknown
test01         test           unknown
dev01          dev            unknown
```

The actual statuses depend on previously saved checks.

## Command-line usage

Use an action argument to run an operation and exit without opening the menu.

| Command | Behavior |
| --- | --- |
| `python3 main.py --help` | Display help and exit. |
| `python3 main.py --list` | Display all servers and exit. |
| `python3 main.py --list --environment prod` | Display production servers only. |
| `python3 main.py --check web01` | Ping the named server, save its status and timestamp, and display its status. |
| `python3 main.py --check-all` | Ping every server, save each result and display the updated table. |
| `python3 main.py --export` | Export all servers to CSV and display the report path. |

Use one action argument per invocation. The `--environment` argument filters `--list` and accepts `dev`, `test` or `prod`:

```bash
# Display development servers.
python3 main.py --list --environment dev

# Check the server without distinguishing uppercase and lowercase letters.
python3 main.py --check WEB01
```

A filtered list with no matches displays only the table header. Invalid environments, unknown arguments and missing argument values are rejected by `argparse`.

## Data file and environment variable

By default, the program loads `servers.json` from the current working directory. Set `INVENTORY_DATAFILE` to use another JSON file:

```bash
# Use an alternative file for this invocation.
INVENTORY_DATAFILE=other_servers.json python3 main.py --list
```

In Bash or Zsh, the variable can also be set for subsequent commands:

```bash
# Use the same alternative data file for the whole terminal session.
export INVENTORY_DATAFILE=other_servers.json
python3 main.py

# Return to the default data file.
unset INVENTORY_DATAFILE
```

Both the menu and CLI use the selected file. Changes are saved to that same file after additions, removals and completed server checks.

If the data file does not exist, the program starts with an empty list. Adding a server then creates the file, provided its parent directory exists. An existing file must contain valid JSON in the expected format; a completely empty file is not the same as an empty list (`[]`).

## Server data format

The JSON file contains a list of server dictionaries. Each server has six string fields:

| Field | Meaning | Example |
| --- | --- | --- |
| `name` | Unique server name, compared case-insensitively when adding. | `web01` |
| `address` | Hostname or IP address used by ping. | `example.com` |
| `environment` | Environment: `dev`, `test` or `prod`. | `prod` |
| `role` | Server role. | `webserver` |
| `status` | Latest ping status: `up`, `down` or `unknown`. | `unknown` |
| `last_checked` | Local check time as `YYYY-MM-DD HH:MM`, or an empty string before the first check. | `""` |

Example record in a valid data file:

```json
[
    {
        "name": "web01",
        "address": "example.com",
        "environment": "prod",
        "role": "webserver",
        "status": "unknown",
        "last_checked": ""
    }
]
```

The supplied inventory contains these four servers. Saved statuses and timestamps may already reflect earlier checks.

| Name | Address | Environment | Role |
| --- | --- | --- | --- |
| `web01` | `example.com` | `prod` | `webserver` |
| `db01` | `127.0.0.1` | `prod` | `database` |
| `test01` | `192.0.2.10` | `test` | `testserver` |
| `dev01` | `localhost` | `dev` | `developmentserver` |

## How server checks work

Each check runs `ping -c 1` with the server's address. The command is passed as a list to `subprocess.run()`, with a five-second process timeout.

- Ping exit code `0` sets the server status to `up`.
- Other ping exit codes and process timeouts set the status to `down`.
- The check time is recorded using the computer's local time as `YYYY-MM-DD HH:MM`.
- The updated server list is saved to JSON after each completed check.

Checks of multiple servers run one at a time. Several servers that time out can therefore take approximately five seconds each.

A failed ping can mean that a firewall or network blocks ping traffic; it does not prove that the server is powered off. A network that blocks internet ping can make `web01` appear down. `db01` and `dev01` point to the local computer.

## CSV reports

Export from menu option `6` or from the command line:

```bash
python3 main.py --export
```

The program creates `reports/` in the current working directory if it does not exist. Report names include the local date and time, for example:

```text
reports/inventory_2026-11-18_1430.csv
```

The report uses UTF-8 and includes the following header and one row per server:

```csv
name,address,environment,role,status,last_checked
```

CSV export includes all servers and their currently saved information; it does not run ping checks. Exporting an empty inventory still writes the header. Exports within the same minute use the same filename and overwrite that report.

## Exit codes

| Code | Meaning |
| --- | --- |
| `0` | Successful listing, export, help or normal menu exit. For CLI checks, all checked servers responded; an empty `--check-all` also returns `0`. |
| `1` | At least one server checked through `--check` or `--check-all` is down or timed out, or the server named with `--check` does not exist. |
| `2` | Invalid CLI arguments, such as an unknown argument, a missing value or an invalid environment. |

The check exit codes apply to CLI operations. Interactive checks return to the menu; they do not close the program based on a server's status.

In Bash or Zsh, inspect the exit code immediately after the command:

```bash
# Check a local server and display the exit code.
python3 main.py --check dev01
echo $?

# An unknown name produces a message and exit code 1.
python3 main.py --check missing
echo $?
```

Completed ping results are saved even when a CLI check returns `1` because a server is down. An unknown server name leaves the data unchanged. Unexpected file or operating system errors may also terminate the program unsuccessfully.

## Project structure

| File | Responsibility |
| --- | --- |
| `main.py` | Entry point, argument parsing, CLI actions, data loading and exit codes. |
| `menu.py` | Menu loop, user input, server management and table display. |
| `storage.py` | JSON loading/saving and CSV export. |
| `checks.py` | Ping execution, status/timestamp updates and checks of all servers. |
| `servers.json` | Server inventory persisted between runs. |
| `.gitignore` | Excludes generated reports, Python cache and local configuration files. |
| [REDOGORELSE.md](REDOGORELSE.md) | Swedish explanation of the code, design choices, sources and tools used. |

For example, both `main.py` and `menu.py` call `checks.check_server()` and `storage.export_servers()`. Updating one of these shared functions changes the behavior for both interfaces.

## Current limitations

- Existing JSON is expected to have valid syntax and all required fields. Malformed JSON or missing keys are not handled with a custom recovery message.
- Empty names, addresses and roles, and spaces inside server names, are not rejected by the add-server form.
- Menu option `4` reports operating system errors from ping or saving. Equivalent error handling is not implemented for all other menu or CLI operations.
