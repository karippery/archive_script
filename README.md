# Archive Group Files

This Python utility archives all non-hidden files from the home directories of users belonging to a specified Linux group.
Files are moved to a central archive directory with a timestamped and random suffix to avoid name collisions.
All operations are logged, and the script is designed for safe, system-wide use.

## Features

* Archives files for all users in a given Linux group
* Supports cross-filesystem moves (e.g., `/home` to `/var`)
* Appends timestamp and random suffix to prevent filename conflicts
* Gracefully handles permission and filesystem errors
* Logs all operations to a central log file
* Can be installed system-wide or packaged as a Debian source package

## Directory Structure

```
archive_script/
├── setup.sh
├── archive_group_files.py
├── config.py
├── logger.py
├── README.md
└── debian/
    └── control
```

## Requirements

* Python 3.6+
* Linux system
* Root privileges (required to access other users’ files)

## Installation

1. **Copy the script to your system**

   ```bash
   mkdir -p ~/archive_script
   cp -r /path/to/archive_script/* ~/archive_script/
   cd ~/archive_script
   ```

2. **Ensure Unix line endings**
   If the script was edited or saved on Windows, convert CRLF to LF:

   ```bash
   sudo apt install dos2unix
   dos2unix *.py setup.sh
   ```

3. **Run the installer**
   Make the setup script executable and run it as root:

   ```bash
   chmod +x setup.sh
   sudo ./setup.sh
   ```

   This will:

   * Install `archive_group_files` into `/usr/local/bin/`
   * Create `/etc/archive_group_files/` for configuration files
   * Create `/var/log/archive_group_files.log` for logs
   * Create `/var/archive_group_files/` as the default archive location

4. **Verify installation**

   ```bash
   archive_group_files --help
   ```

## Usage

Run the script with the target Linux group as an argument:

```bash
sudo archive_group_files developers
```

This will:

* Identify all users in the `developers` group
* Move their non-hidden home directory files into `/var/archive_group_files/developers/`
* Append a timestamp and random suffix to avoid filename collisions
* Record the operation in the log file

### Log File

Default log location:

```
/var/log/archive_group_files.log
```

Example log entry:

```
2025-08-07 23:54:08,783 INFO: [run_id=15ac0a] Found 2 members in group 'developers'.
2025-08-07 23:54:08,784 INFO: [run_id=15ac0a] Moved '/home/alice/alice1.txt' to '/var/archive_group_files/developers/alice/alice1.txt.20250807235408_c9cae3'
2025-08-07 23:54:08,785 INFO: [run_id=15ac0a] Moved '/home/bob/bob2.txt' to '/var/archive_group_files/developers/bob/bob2.txt.20250807235408_8502d4'
2025-08-07 23:54:08,785 INFO: [run_id=15ac0a] Archived 2 files for 2 users in group 'developers'
```

## Parallel Execution Safety
If there is a chance that the script might be executed concurrently (for example, by cron or in a distributed system), you should add a simple file lock to avoid race conditions.
This can be done with fcntl

## Debian Packaging

The `debian/` directory contains the control file for building a Debian package.
You can install using `setup.sh` directly or build with tools like `dpkg-deb`.

