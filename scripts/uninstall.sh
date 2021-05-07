#!/bin/bash

# Stop running if any program errors
set -e

# Find absolute path of scripts
curr_path=$PWD
cd ${BASH_SOURCE%/*}
script_path=$PWD
cd ${curr_path}

# Remove virtual environment, update script, cron task
yes | rm -r ${script_path}/../env/venv-rss
echo "1. Removed virtual environment"

rm ${script_path}/rss_update.sh
echo "2. Removed rss_update.sh"

crontab -l | grep -v "rss_update.sh" |crontab -
echo "3. Removed rss_update.sh from cron"