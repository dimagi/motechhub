from connected_accounts.account_interface import AccountManager
from connected_accounts.commcarehq.models import CommCareAccountInfo, \
    CommCareAccountUserDisplay, CommCareAccountUserInput


commcarehq_account_manager = AccountManager(
    account_type='commcarehq',
    info_class=CommCareAccountInfo,
    user_display_class=CommCareAccountUserDisplay,
    user_input_class=CommCareAccountUserInput,
)
