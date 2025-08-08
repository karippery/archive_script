#!/usr/bin/env python3

import os
import sys
import shutil
import pwd
import grp
import uuid
import errno
import argparse
from datetime import datetime
from pathlib import Path

sys.path.insert(0, "/etc/archive_group_files")

from config import ARCHIVE_BASE_DIR, LOG_FILE
from logger import get_logger




def safe_move(src: str, dst: str):
    """
    Move a file safely across filesystems.
    Falls back to copy + delete if needed.
    """
    try:
        shutil.move(src, dst)
    except OSError as e:
        if e.errno == errno.EXDEV:  # Cross-device move
            try:
                shutil.copy2(src, dst)
                os.unlink(src)
            except Exception as inner_e:
                if Path(dst).exists():
                    Path(dst).unlink()  # Clean up partial file
                raise inner_e
        else:
            raise


def prepare_archive_dir(logger):
    """
    Ensures the archive base directory is writable.
    """
    try:
        Path(ARCHIVE_BASE_DIR).mkdir(parents=True, exist_ok=True)
        test_file = Path(ARCHIVE_BASE_DIR) / ".test_write"
        test_file.touch()
        test_file.unlink()
    except OSError as e:
        logger.error(f"Cannot access archive directory: {e.strerror} (errno={e.errno})")
        sys.exit(1)


def get_group_members(group_name: str, logger):
    """
    Returns the usernames in the given group.
    """
    try:
        return grp.getgrnam(group_name).gr_mem
    except KeyError:
        logger.error(f"Group '{group_name}' does not exist.")
        sys.exit(1)
    except PermissionError:
        logger.error("Permission denied when accessing group info.")
        sys.exit(1)


def process_user(username: str, group_name: str, logger):
    """
    Archives the user’s files and returns the count of files moved.
    """
    try:
        user_info = pwd.getpwnam(username)
    except KeyError:
        logger.warning(f"User '{username}' not found, skipping.")
        return 0

    user_home = Path(user_info.pw_dir)
    if not user_home.exists():
        logger.warning(f"Home dir for '{username}' not found, skipping.")
        return 0

    archive_dir = Path(ARCHIVE_BASE_DIR) / group_name / username
    archive_dir.mkdir(parents=True, exist_ok=True)

    file_count = 0
    for file in user_home.iterdir():
        if file.is_file() and not file.name.startswith('.'):
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            unique_id = uuid.uuid4().hex[:6]
            dest = archive_dir / f"{file.name}.{timestamp}_{unique_id}"
            try:
                safe_move(str(file), str(dest))
                file_count += 1
                logger.info(f"Moved '{file}' to '{dest}'")
            except Exception as e:
                logger.error(f"Failed to move '{file}': {e}")
    return file_count


def archive_group_files(group_name: str, logger):
    """
    Archives files of all members of a specified group.
    """
    if os.geteuid() != 0:
        logger.error("This script must be run as root.")
        sys.exit(1)

    prepare_archive_dir(logger)
    members = get_group_members(group_name, logger)
    logger.info(f"Found {len(members)} members in group '{group_name}'.")

    total_files = 0
    users_with_files = 0

    for user in members:
        count = process_user(user, group_name, logger)
        if count:
            total_files += count
            users_with_files += 1

    logger.info(f"Archived {total_files} files for {users_with_files} users in group '{group_name}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Archive files of a user group.")
    parser.add_argument("group", help="The name of the group to archive files for.")
    args = parser.parse_args()

    # Setup logger with run ID
    RUN_ID = uuid.uuid4().hex[:6]
    logger = get_logger(LOG_FILE, run_id=RUN_ID)

    archive_group_files(args.group, logger=logger)
