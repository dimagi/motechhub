import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from connected_accounts.account_interface import get_account_manager


class ConnectedAccountsView(TemplateView):
    template_name = 'connected_accounts/connected_accounts.html'

    def get_context_data(self, **kwargs):
        context = super(ConnectedAccountsView, self).get_context_data(**kwargs)
        context.update({
            'connected_accounts': []
        })
        return context


@csrf_exempt
@require_POST
def save_connected_account(request, domain):
    post_body_json = json.loads(request.body)
    account_type = post_body_json['account_type']
    account_manager = get_account_manager(account_type)
    account = account_manager.save_user_input(domain, post_body_json)
    return JsonResponse(account.to_json())
