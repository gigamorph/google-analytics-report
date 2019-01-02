#!/bin/sh

# Import environment variables
. ./env.sh

python --version
pip --version

# Install virtualenv
if ! virtualenv --version; then
  echo "Installing virtualenv"
  pip install virtualenv
fi

echo "virtualenv: $(virtualenv --version)"

# Create the virtual python environment.
if [ ! -f $PYTHON_ENV ]; then
  echo "Creating virtualenv at $PYTHON_ENV"
  virtualenv $PYTHON_ENV
fi

# Output files will be generated here.
if [ ! -d $OUTPUT_DIR ]; then
  echo "Creating directory $OUTPUT_DIR"
  mkdir $OUTPUT_DIR
fi

# Log will be written here.
if [ ! -d $LOG_DIR ]; then
  echo "Creating directory $LOG_DIR"
  mkdir $LOG_DIR
fi

# Symlink the tokens folder.
echo "TOKENS DIR: $TOKENS_DIR"
if [ -n "$TOKENS_DIR" ] && [ -d $TOKENS_DIR ]; then
  ln -s $TOKENS_DIR $CONFIG_DIR/tokens
else
  echo "Error: tokens dir [$TOKENS_DIR] does not exist."
  exit 1
fi

echo "Activating virtualenv: ${PYTHON_ENV}/bin/activate"
. $PYTHON_ENV/bin/activate

# Install python modules
pip install --no-deps -r pip_requirements.txt
