"""
Extract information from Google Analytics
"""

import sys

import argparse
import logging
import re

from oauth2client.tools import argparser

from config_manager import ConfigManager
from reporter import Reporter


class App(object):

    def __init__(self):
        self.args = self.parse_args()

    def parse_args(self):
        """Parse command-line arguments"""
        parser = argparse.ArgumentParser(
            description=__doc__,
                                         formatter_class=argparse.RawDescriptionHelpFormatter,
                                         parents=[argparser])
        #parser.add_argument('--params', type=str, help='File containing query parameters')
        #parser.add_argument('--start', type=str, help='Start date')
        #parser.add_argument('--end', type=str, help='End date')

        args = parser.parse_args(sys.argv[1:])
        return args

    def get_query_params(self):
        """
        Each line looks like
        key = value
        with an optional end of line comment that begins with a "#".
        """

        fpath = self.args.params
        params = dict()
        with open(fpath, 'r') as f:
            for line in f:
                line2 = re.sub(r'^([^#]*)#.*$', r'\1', line) #remove comment
                m = re.match(r'\s*(\S+?)\s*=\s*(\S+)', line2)
                if m:
                    key = m.group(1)
                    value = m.group(2)
                    params[key] = value
                elif line2.strip() != '': #not a pure comment line nor an empty line
                    logging.warning('Invalid line: %s' % line)
        return params

    def run(self):
        """The main routine of the app"""
        config_manager = ConfigManager(self.args)
        reporter = Reporter(config_manager)
        reporter.run()

        #params = self.get_query_params()
        #params['start'] = self.args.start
        #params['end'] = self.args.end

        #print(json.dumps(reporter.get_report(params), sort_keys=True, indent=2))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = App()
    app.run()
