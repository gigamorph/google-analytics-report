#!/bin/sh

RECIPIENTS=${EMAIL_RECIPIENTS} # separated by spaces

echo "Downloading data and generating reports..."
./gen_reports.sh

if [ $? -ne 0 ]; then
  echo 'See log attached.' | mail -s 'GoogleAnalyticsApp: Failed to get reports' -a ../log/analytics.log $RECIPIENTS
  exit 1
fi

echo "Sending reports to MFT..."
./send_files.sh

if [ $? -ne 0 ]; then
  echo 'See logs attached.' | mail -s 'GoogleAnalyticsApp: Failed to send reports' -a ../log/analytics.log -a ../log/send_files.log $RECIPIENTS
  exit 1
fi

echo 'See logs attached.' | mail -s 'GoogleAnalyticsApp: Success' -a ../log/analytics.log -a ../log/send_files.log $RECIPIENTS
