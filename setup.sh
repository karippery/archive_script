#!/bin/bash

set -e

SCRIPT_NAME="archive_group_files"
INSTALL_PATH="/usr/sbin"
CONFIG_DIR="/etc/archive_group_files"
LOG_FILE="/var/log/archive_group_files.log"

# Privilege check
if [ "$EUID" -ne 0 ]; then
  echo "This installer must be run as root"
  exit 1
fi

echo "Installing $SCRIPT_NAME..."

# 1. Create config directory
mkdir -p "$CONFIG_DIR"

# 2. Install Python script to /usr/sbin
cp "$SCRIPT_NAME.py" "$INSTALL_PATH/$SCRIPT_NAME"
chmod +x "$INSTALL_PATH/$SCRIPT_NAME"

# 3. Install config files, ask before overwrite
for file in config.py logger.py; do
  if [ -f "$CONFIG_DIR/$file" ]; then
    echo "$file already exists in $CONFIG_DIR. Overwrite? [y/N]"
    read -r ans
    if [[ "$ans" != "y" && "$ans" != "Y" ]]; then
      echo "Skipping $file"
      continue
    fi
  fi
  cp "$file" "$CONFIG_DIR/"
done

# 4. Create log file if it doesn’t exist
touch "$LOG_FILE"
chmod 644 "$LOG_FILE"

echo "Installed $SCRIPT_NAME"
echo "Run it with: sudo $SCRIPT_NAME <groupname>"
