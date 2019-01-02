#!/bin/sh

. ./env.sh

if [ -d "$LOG_DIR" ]; then
  LOG=../log/analytics.log
else
  echo "Log directory $LOG_DIR does not exist. Writing only to stdout"
  LOG=/dev/null
fi

echo "BEGIN: $(date)" | tee $LOG

echo "Activating virtualenv: ${PYTHON_ENV}/bin/activate" | tee -a $LOG
source $PYTHON_ENV/bin/activate 2>&1 | tee -a $LOG

now=$(date)

# If START_DATE and END_DATE are not specified, set the range to the past week.
# The date calculation syntax was tested only on Linux.
# It doesn't work on, i.e., MacOS.
# Set START_DATE and END_DATE explicitly in that case.
if [ "$START_DATE" = "" ]; then
  START_DATE=$(date -d "$now-7days" +"%Y-%m-%d")
  export START_DATE
fi

if [ "$END_DATE" = "" ]; then
  END_DATE=$(date -d "$now-1days" +"%Y-%m-%d")
  export END_DATE
fi

echo "Date range: $START_DATE through $END_DATE" | tee -a $LOG

echo "Output files are being created in ${OUTPUT_DIR}" | tee -a $LOG
python $SCRIPT_ROOT/main.py --noauth_local_webserver 2>&1 | tee -a $LOG

if [ $PIPESTATUS -ne 0 ]; then
  exit 1
fi

echo "END: $(date)" 2>&1 | tee -a $LOG
