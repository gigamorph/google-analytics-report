"""This module contains the Reporter class"""
import os.path
import random
import socket
import time

from apiclient.errors import HttpError
from management_api import ManagementAPI

class Reporter(object):
    """Retrieve analytics data and generate CSV report files"""

    separator = '|||'
    master_header = ['profileId', 'profileName', 'webPropertyId',
                     'webPropertyName', 'webPropertyURL', 'accountId',
                     'accountName', 'gmail']

    def __init__(self, config_manager):
        config_manager = config_manager
        config = config_manager.config

        self.outdir = config['output_dir']
        self.groups = config['report_profiles']
        self.start_date = config['start_date']
        self.end_date = config['end_date']

        self.services = config_manager.get_services()
        self.profiles = set() # stores profile IDs to prevent duplicate data.

    def run(self):
        """Main method of Reporter"""
        self._open_files()
        self._report()
        self._close_files()

    def _open_files(self):
        master_file_path = os.path.join(self.outdir, 'Master.csv')
        self.master_file = open(master_file_path, 'w')
        self.group_files = dict()

        for group in self.groups:
            key = group['name']
            self.group_files[key] = open(os.path.join(self.outdir, key + '.csv'), 'w')

    def _close_files(self):
        self.master_file.close()
        for k, gfile in self.group_files.iteritems():
            gfile.close()

    def _report(self):
        """Retrieve data and write to the files"""
        self.master_file.write(Reporter.separator.join(Reporter.master_header) + '\n')

        for group in self.groups:
            key = group['name']
            self.group_files[key].write(self._create_group_header(group))

        for service in self.services:
            self._report_for_service(service)

    def _report_for_service(self, service):
        mgmt = ManagementAPI(service)
        account_items = mgmt.get_account_items()
        for account_item in account_items:
            print 'Processing account [%s]' % account_item.get('name')
            account_id = account_item['id']
            webproperty_items = mgmt.get_webproperty_items(account_id)
            time.sleep(0.1)
            for webproperty_item in webproperty_items:
                print 'Processing web property [%s: %s]' % (webproperty_item['name'], webproperty_item['id'])
                webproperty_id = webproperty_item['id']
                try:
                    profile_items = mgmt.get_profile_items(account_id, webproperty_id)
                    time.sleep(0.1)
                except HttpError, e:
                    print 'ERROR getting profile items for account_id: %s, webproperty_id: %s' % (account_id, webproperty_id)
                    print 'Error: %s' % e
                    continue
                for profile_item in profile_items:
                    profile_id = profile_item['id']
                    if profile_id in self.profiles:
                        print 'Skipping duplicate profile:'
                        print '- profile: %s (%s)' % (profile_item['name'], profile_id)
                        print '- property: %s (%s)' % (webproperty_item['name'], webproperty_item['id'])
                    else:
                        self._report_for_profile(service, account_item, webproperty_item, profile_item)
                        time.sleep(0.1)
                        self.profiles.add(profile_id)

    def _report_for_profile(self, service, account_item, webproperty_item, profile_item):
        self.master_file.write(self._master_header(account_item, webproperty_item, profile_item))

        for group in self.groups:
            result = self._request_with_backoff(service, profile_item, group['dimensions'], group['metrics'])
            self._write_result(result, self.group_files[group['name']])

    def _master_header(self, account_item, webproperty_item, profile_item):
        a, w, p = account_item, webproperty_item, profile_item
        url = w.get('websiteUrl') or ''
        columns = [p['id'], p['name'], w['id'], w['name'], url, a['id'], a['name'], 'yale.metrics@gmail.com']
        return self.separator.join(columns) + '\n'

    def _create_group_header(self, group):
        csv = 'profileId,' + group['dimensions'].replace('ga:', '') + ',' + group['metrics'].replace('ga:', '')
        return Reporter.separator.join(csv.split(',')) + '\n'

    def _write_result(self, result, f):
        rows = result.get('rows')
        if rows:
            id = result.get('profileInfo').get('profileId')
            for row in rows:
                line = Reporter.separator.join([id] + row) + '\n'
                f.write(line.encode('ascii', 'ignore').decode('ascii'))
        else:
            # do nothing because there is no data
            return

    def _request_with_backoff(self, service, profile, dimensions, metrics):
        """Wrapper to request Google Analytics data with exponential backoff.

        Accepts the analytics service object, makes API requests and
        returns the response. If any error occurs, the request is retried
        using exponential backoff.
        """

        for n in range(0, 5):
            try:
                return self._get_result(service, profile, dimensions, metrics)
            except HttpError as e:
                print('HttpError %s' % e.resp.reason)
                #if e.resp.reason in ['userRateLimitExceeded', 'quotaExceeded']:
                wait_time = (2 ** n) + random.random()
                print('Waiting for %.2f seconds' % wait_time)
                #print('Rate limit exceeded: waiting for %.2f seconds' % wait_time)
                time.sleep(wait_time)
            except socket.error as e:
                print('Socket error %s' % str(e))
                wait_time = (2 ** n) + random.random()
                print('Waiting for %.2f seconds' % wait_time)
                time.sleep(wait_time)

        print 'ERROR Reporter#request_with_backoff: the request never succeeded.'

    def _get_result(self, service, profile, dimensions, metrics):
        # Use the Analytics Service Object to query the Core Reporting API
        return service.data().ga().get(
            ids='ga:' + profile['id'],
            start_date=self.start_date,
            end_date=self.end_date,
            dimensions=dimensions,
            metrics=metrics).execute()
