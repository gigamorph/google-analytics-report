#!/bin/sh

. ./env.sh

if [ -d "$LOG_DIR" ]; then
  LOG=../log/send_files.log
else
  echo "Log directory $LOG_DIR does not exist. Writing only to stdout"
  LOG=/dev/null
fi

echo "Sending reports to MFT." | tee $LOG
echo "BEGIN: $(date)" | tee -a $LOG

BATCH_FILE=./send_files_batch.txt

if [ -n "$ID_FILE" ]; then
  if [ -f "$ID_FILE" ]; then
    ID_OPT="-i $ID_FILE"
  else
    echo "SSH id file not found at $ID_FILE. Trying to use the default." | tee -a $LOG
    ID_OPT=''
  fi
else
  echo "SSH id file not specified. Trying to use the default." | tee -a $LOG
  ID_OPT=''
fi

sftp $ID_OPT -b $BATCH_FILE ${MFT_USER}@${MFT_HOST} 2>&1 | tee -a $LOG

if [ $PIPESTATUS -ne 0 ]; then
  exit 1
fi

echo "END: $(date)" | tee -a $LOG
