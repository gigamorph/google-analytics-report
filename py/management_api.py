"""Wrapper of Google Analytics Management API"""


class ManagementAPI(object):
    """Wrapper of Google Analytics Management API"""

    def __init__(self, service):
        self.api = service.management()

    def get_accounts(self):
        return self.api.accounts().list().execute()

    def get_account_items(self):
        accounts = self.get_accounts()
        return accounts.get('items')

    def get_account(self, account_name):
        account_items = self.get_account_items()
        filtered = filter(lambda x: x.get('name') == account_name,
                          account_items)
        count = len(filtered)
        if count == 1:
            return filtered[0]
        elif count == 0:
            return None
        else:
            raise RuntimeError('ManagementAPI#get_account - got %d accounts, expected 1.' % count)

    def get_webproperty_items(self, account_id):
        webproperties = self.api.webproperties().list(accountId=account_id).execute()
        return webproperties.get('items')

    def get_webproperty(self, account_id, webproperty_id):
        webproperty_items = self.get_webproperty_items(account_id)
        filtered = filter(lambda x: x.get('id') == webproperty_id,
            webproperty_items)
        count = len(filtered)
        if count == 1:
            return filtered[0]
        elif count == 0:
            return None
        else:
            raise RuntimeError('GAProxy#get_webproperty - got %d webproperties, expected 1.' % count)

    def get_profile_items(self, account_id, webproperty_id):
        profiles = self.api.profiles().list(
            accountId=account_id,
            webPropertyId=webproperty_id).execute()
        return profiles.get('items')

    def get_profile(self, account_id, webproperty_id, profile_name):
        profile_items = self.get_profile_items(account_id, webproperty_id)
        filtered = filter(lambda x: x.get('name') == profile_name,
            profile_items)
        count = len(filtered)
        if count == 1:
            return filtered[0]
        elif count == 0:
            return None
        else:
            raise RuntimeError('GAProxy#get_profile - got %d profiles, expected 1.' % count)

    def get_profile_id(self, account_id, webproperty_id, profile_name):
        profile = self.get_profile(account_id, webproperty_id,
            profile_name)
        return profile.get('id')

    def delete_profile(self, account_id, webproperty_id, profile_name):
        profile_id = self.get_profile_id(account_id, webproperty_id, profile_name)
        self.api.profiles().delete(accountId=account_id,
                                   webPropertyId=webproperty_id,
                                   profileId=profile_id).execute()
