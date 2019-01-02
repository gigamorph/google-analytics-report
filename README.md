# Analytics

## Installation

### Requirements
* Bash
* Python (2.7 <= version < 3.0)
* Python modules
  * google-api-python-client
* Google Analytics account(s)

### Install Google API Python Client

Install the Google API Python Client using ```sudo pip install --upgrade google-api-python-client``` on the unix terminal. If you don't have a unix terminal, download the latest [client library for python](https://pypi.python.org/pypi/google-api-python-client/) and run ```setup.py``` with ```install``` as the argument.

Note: On a Mac, you might have to install and run a [virtual environment for python](http://docs.python-guide.org/en/latest/dev/virtualenvs/) since there are some python module importing issues. You would install the google api python client within that environment.

### Configuration
* Copy ```config/config.json.template``` to ```config/config.json``` and
  modify it according to your account information and reporting needs.
* Create a "client secrets" file per Google Analytics account using ```client_secrets.json.template``` under ```config/client_secrets```.

### Initial Run

1. Log onto the gmail that is associated with the ```client_secrets.json```
2. Run ```gen_report.sh``` under ```bin/``` directory and follow the instructions to get and enter the verification code for each Google Analytics account. That will create token file(s) under ```config/tokens/```.

## Running

Once the tokens are installed, you can run ```bin/gen_report.sh``` anytime without authenticating. Keep the token files in a secure place.

Example:
```
START_DATE=2015-10-12 END_DATE=2015-10-19 gen_report.sh 2>&1 > my.log
```

The parameters ```START_DATE``` and ```END_DATE``` are passed as environment variables.
