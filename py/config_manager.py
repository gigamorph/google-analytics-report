import os
import json

from google_auth import GoogleAuth


class ConfigManager(object):

    def __init__(self, auth_flags):
        self.auth_flags = auth_flags
        self.config = dict()
        self._get_env()

        with open(os.path.join(self.config['config_dir'], 'config.json')) as config_file:
            self.config.update(json.loads(config_file.read()))

        self.config['auth_scope'] = ['https://www.googleapis.com/auth/analytics.readonly']

    def get_service(self, auth_profile):
        """ Build Google Analytics service for the auth profile """
        app_root = self.config['app_root_dir']
        client_secrets_path = os.path.join(app_root, auth_profile['client_secrets_path'])
        token_path = os.path.join(app_root, auth_profile['token_path'])
        auth = GoogleAuth(self.auth_flags, client_secrets_path, token_path)
        service = auth.build_service('analytics', 'v3')
        return service

    def get_services(self):
        """ Return list of services for all auth profiles """

        services = []

        for p in self.config['auth_profiles']:
            services.append(self.get_service(p))
        return services

    def _get_env(self):
        self.config['app_root_dir'] = os.environ['APP_ROOT']
        self.config['config_dir'] = os.environ['CONFIG_DIR']
        self.config['output_dir'] = os.environ['OUTPUT_DIR']
        self.config['start_date'] = os.environ['START_DATE']
        self.config['end_date'] = os.environ['END_DATE']

    def _find_auth_profile(self, auth_profile_id):
        for p in self.config['auth_profiles']:
            if p['id'] == auth_profile_id:
                return p
        return None
