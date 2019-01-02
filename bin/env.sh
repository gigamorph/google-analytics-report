#!/bin/sh

echo "Current directory: $(pwd)"

PYTHON_ENV=$HOME/.virtualenvs/analytics

APP_ROOT=..
SCRIPT_ROOT=$APP_ROOT/py

export PYTHONPATH=$SCRIPT_ROOT
echo "PYTHONPATH: $PYTHONPATH"

export APP_ROOT
export CONFIG_DIR=$APP_ROOT/config
export DUMMY_SECRETS_PATH=$CONFIG_DIR/client_secrets/client_secrets.json.template
export OUTPUT_DIR=$APP_ROOT/output
export LOG_DIR=$APP_ROOT/log
