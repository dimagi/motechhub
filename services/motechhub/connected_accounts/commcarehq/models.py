from __future__ import unicode_literals

import jsonobject
import authproxy_client


class StrictJsonObject(jsonobject.JsonObject):
    _allow_dynamic_properties = False
    _string_conversions = ()


class CommCareAccountInfo(StrictJsonObject):
    account_type = 'commcarehq'
    url = jsonobject.StringProperty()
    domain = jsonobject.StringProperty()
    username = jsonobject.StringProperty()


class CommCareAccountUserDisplay(CommCareAccountInfo):
    id = jsonobject.StringProperty()


class CommCareAccountUserInput(CommCareAccountUserDisplay):
    api_key = jsonobject.StringProperty()

    def to_account_info(self):
        return CommCareAccountInfo(url=self.url, domain=self.domain, username=self.username)

    def to_credential(self):
        return authproxy_client.Credential(
            target=self.url,
            auth=authproxy_client.ApiKeyAuth(
                username=self.username,
                apikey=self.api_key
            )
        )
