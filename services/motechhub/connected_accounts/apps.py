from __future__ import unicode_literals

from django.apps import AppConfig


class ConnectedAccountsConfig(AppConfig):
    name = 'connected_accounts'

    def ready(self):
        from connected_accounts.account_interface import register_account_manager
        from connected_accounts.commcarehq import commcarehq_account_manager
        register_account_manager(commcarehq_account_manager)
