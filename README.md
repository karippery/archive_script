# Archive Group Files Script

This Python script archives all non-hidden files from the home directories of users belonging to a specified Linux group. The files are moved to a central archive directory, with timestamped filenames to prevent collisions. The script is designed to be robust, logged, and safe for system-wide usage.



##  Features

- Archives files for all users in a given Linux group
- Supports cross-filesystem moves (`/home` to `/var`, etc.)
- Adds timestamp and random suffix to avoid filename collisions
- Handles permission and filesystem errors gracefully
- Logs all operations and errors to a central log file
- Ready to be packaged as a Debian source package



## Directory Structure

    archive_script/
    ├── setup.sh
    ├── archive_group_files.py  
    ├── config.py                
    ├── logger.py                   
    ├── README.md               
    └── debian/
        └── control





## Usage


## Install with setup.sh (must be run as root)

Make the installer executable and run it:

```bash
chmod +x setup.sh
sudo ./setup.sh
```

if  script was saved on Windows, so it uses CRLF line endings. Linux expects LF only.

```bash
sudo apt install dos2unix
dos2unix archive_group_files.py
```

### 1. Run the script (must be root)


```bash
sudo  archive_group_files developers
```

### 2. Log File

By default, all operations are logged to:

```
/var/log/archive_group_files.log
```

Example log entry:

```
2025-08-06 13:22:10,120 [INFO]: Moved '/home/alice/report.txt' to '/var/archive_group_files/developers/alice/report.txt.20250806132210123_ab12cd'
```


## Requirements

* Python 3.6+
* Linux system
* Must be run as root (to access all home directories)





## Debian Packaging

The `debian/` folder contains the required control file to build a source package. You can install it manually using `setup.sh` or build with tools like `dpkg-deb`.


## License


