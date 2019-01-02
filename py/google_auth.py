import httplib2
import logging
import os

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client.tools import run_flow


class GoogleAuth(object):

    def __init__(self, auth_flags, client_secrets_path, token_file_path):
        self.flags = auth_flags
        self.token_file_path = token_file_path
        scope = 'https://www.googleapis.com/auth/analytics.readonly'

        try:
            self.flow = flow_from_clientsecrets(client_secrets_path, scope,
                message='Client secrets file is missing: [%s]' % client_secrets_path)
        except SystemExit as e:
            logging.info(e.message)
            dummy_secrets_path = os.environ['DUMMY_SECRETS_PATH']
            logging.info('Loading dummy secrets to create a flow: %s' % dummy_secrets_path)
            self.flow = flow_from_clientsecrets(dummy_secrets_path, scope,
                message='Dummy secrets file is missing: [%s]' % dummy_secrets_path)

    def prepare_credentials(self, token_file_path):
        storage = Storage(token_file_path)
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = run_flow(self.flow, storage, self.flags)

        return credentials

    def build_service(self, service_name, version):
        http = httplib2.Http()
        credentials = self.prepare_credentials(self.token_file_path)
        http = credentials.authorize(http)
        return build(service_name, version, http=http)
