# Server Inventory Tool

A Python command-line program for tracking server names, addresses, environments, roles, statuses and check timestamps.

> **Status:** The text menu supports listing, filtering, adding, removing and checking servers. JSON changes are saved after each update. CSV export is available through menu option 6. All required CLI arguments are implemented: --help, --list, --environment, --check, --check-all and --export. The written explanation and final submission checks are still outstanding.

**Assignment target:** G. VG extensions and REFLEKTION.md are not required for this submission.

## Requirements

- Python 3.
- No external Python packages; the program uses only the standard library.
- The `ping` command must be available. The current flags support Linux/macOS.

## Running the program

Run from the project directory because the default data path is relative to the current working directory:

```bash
python3 main.py
```

The menu repeats after each operation until you choose `0`.

| Option | Action |
| --- | --- |
| `1` | List all servers. |
| `2` | Add a server. Invalid environments are rejected, duplicate names are blocked, and the initial status is `unknown`. |
| `3` | Remove a server. Production servers require confirmation with `yes`. |
| `4` | Check a named server using ping. |
| `5` | Check all servers and display their updated statuses. |
| `6` | Export all servers to CSV and display the saved report path. |
| `7` | List servers in a selected environment. |
| `0` | Exit. |

Server names are compared without distinguishing uppercase and lowercase letters. Environments must be `dev`, `test` or `prod`.

The table uses aligned columns:

```text
Name           Environment    Status
web01          prod           unknown
db01           prod           unknown
test01         test           unknown
dev01          dev            unknown
```

## Environment variable

`INVENTORY_DATAFILE` selects the JSON data file. The default is `servers.json`.

```bash
INVENTORY_DATAFILE=other_servers.json python3 main.py
```

If the file is missing, the program starts with an empty list. Listing then displays only the header row. Adding a server creates the data file, provided its parent directory exists.

## Data file

`servers.json` contains a list of dictionaries, each with six keys:

| Key | Content | Example |
| --- | --- | --- |
| `name` | Server name | `web01` |
| `address` | Hostname or IP address | `example.com` |
| `environment` | Environment: `dev`, `test` or `prod` | `prod` |
| `role` | Server role | `webserver` |
| `status` | Status: `up`, `down` or `unknown` | `unknown` |
| `last_checked` | Latest check time, or an empty string if never checked | `""` |

## Server checks

A check sends one ping packet and allows approximately five seconds for the process to finish. Exit code `0` produces `up`; other exit codes and timeouts produce `down`. A failed ping can also mean that the network blocks ping traffic.

Each completed check records the computer's local time as `YYYY-MM-DD HH:MM` and saves the entire server list to JSON. Menu option 4 reports operating system errors, such as a missing ping command or a failed save. Option 5 does not yet have equivalent error handling.

## CSV export function

`storage.export_servers(servers)` creates `reports/` if needed, writes a header and one row per server, and returns the report path. It uses UTF-8 and names files like `inventory_2026-11-12_1430.csv`. Exports within the same minute use the same filename and overwrite the previous report.

Choose menu option 6 or run python3 main.py --export to export all servers and display the report path.

## Project structure

| File | Responsibility |
| --- | --- |
| `main.py` | Entry point, argument parsing, CLI dispatch, data loading and exit codes. |
| `menu.py` | Menu loop, user input and server display. |
| `storage.py` | JSON loading and saving, and CSV export. |
| `checks.py` | Ping checks, status updates and timestamps. |
| `servers.json` | Server data. |
| `REDOGORELSE.md` | Swedish written explanation template for the G requirements; answers must be written in the author's own words. |
| `REFLEKTION.md` | Optional VG reflection template; not required for the selected G target. |

## CLI support

Run without arguments to start the menu. Action arguments run the selected operation and exit without opening the menu.

| Command | Behavior |
| --- | --- |
| `python3 main.py` | Start the text menu. |
| `python3 main.py --help` | Display help and exit. |
| `python3 main.py --list` | List all servers and exit. |
| `python3 main.py --list --environment prod` | Display production servers only. Use dev or test for those environments. |
| `python3 main.py --check web01` | Ping the named server, save its status and timestamp, and display its status. |
| `python3 main.py --check-all` | Ping every server, save each result and timestamp, and display the table. |
| `python3 main.py --export` | Export all servers to CSV and display the saved report path. |

The --environment argument accepts dev, test or prod and filters --list. Server names for --check are matched without distinguishing uppercase and lowercase letters. Use one action argument per invocation.

## Exit codes

| Code | Meaning |
| --- | --- |
| `0` | The operation succeeded. For --check or --check-all, every checked server responded; an empty check-all also returns 0. |
| `1` | At least one checked server did not respond or timed out, or the server named with --check does not exist. |
| `2` | argparse rejected an invalid or unknown argument, a missing argument value, or an unsupported environment. |

Successful listing and normal menu exit return 0 automatically. Check and export branches use sys.exit() explicitly. Unexpected file or operating system errors can also terminate the program unsuccessfully.

In Bash or Zsh, inspect the code immediately after execution:

```bash
# Check the server and display the process exit code.
python3 main.py --check dev01
echo $?
```

A nonzero check result does not prevent completed status and timestamp updates from being saved to JSON. An unknown server name leaves the data unchanged.
