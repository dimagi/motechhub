from collections import namedtuple
import os
import uuid
from connected_accounts.models import ConnectedAccount
from motechhub.globals import authproxy_client


class AccountManager(
    namedtuple('AccountManager',
               ['account_type', 'info_class', 'user_display_class', 'user_input_class'])):

    def save_user_input(self, domain, json_post_body):
        account_type = json_post_body['account_type']
        assert account_type == self.account_type
        user_input = self.user_input_class.wrap(json_post_body)
        if user_input.id:
            token = uuid.UUID(user_input.id)
            try:
                pk = ConnectedAccount.objects.get(token=token, domain=domain).pk
            except ConnectedAccount.DoesNotExist:
                raise ValueError("Not a valid token: {}".format(token))
        else:
            pk = None
            token = uuid.uuid4()

        account_info = user_input.to_account_info().to_json()

        connected_account = ConnectedAccount(
            pk=pk,
            domain=domain,
            account_type=account_type,
            token=token,
            # os.urandom for cryptographically-random 128-bit key
            token_password=os.urandom(16),
            account_info=account_info,
        )
        connected_account.save()

        credential = user_input.to_credential()
        authproxy_client.create_or_update_credential(
            token, target=credential.target, auth=credential.auth)

        return self.user_display_class(id=str(token), **account_info)


_account_managers = {}


def register_account_manager(account_manager):
    _account_managers[account_manager.account_type] = account_manager


def get_account_manager(account_type):
    return _account_managers[account_type]
