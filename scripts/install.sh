#!/bin/bash

# Stop running if any program errors
set -e

# Find absolute path of scripts
curr_path=$PWD
cd ${BASH_SOURCE%/*}
script_path=$PWD
cd ${curr_path}

# Create Python3 virtual environment
echo "1. Creating Python3 virtual environment"
python3 -m venv ${script_path}/../env/venv-rss
source ${script_path}/../env/venv-rss/bin/activate
pip -q install wheel
pip -q install -r ${script_path}/../env/requirements.txt
deactivate

# Create script to update RSS filter
echo "2. Creating script to update filtered RSS feed"
if ! [ -e ${script_path}/rss_update.sh ]
then
    touch ${script_path}/rss_update.sh
    echo '#!/bin/bash' >>  ${script_path}/rss_update.sh
    echo "source $script_path/../env/venv-rss/bin/activate" >>  ${script_path}/rss_update.sh
    echo "python $script_path/../program/rss_feed_filter.py" >>  ${script_path}/rss_update.sh
    echo 'deactivate' >> ${script_path}/rss_update.sh
fi

# Run script once to confirm it works
echo "3. Verifying script functionality"
chmod +x ${script_path}/rss_update.sh
source ${script_path}/rss_update.sh

# Add update script to cron to autoupdate every 3 hours
(crontab -l; echo "0 */3 * * * ${script_path}/rss_update.sh") | awk '!x[$0]++' |crontab -
# Repeat crontab command twice if first use of cron on system
(crontab -l; echo "0 */3 * * * ${script_path}/rss_update.sh") | awk '!x[$0]++' |crontab -
echo "4. Added ${script_path}/rss_update.sh to cron"
echo -e "\tCron task scheduled to run every 3 hours"
