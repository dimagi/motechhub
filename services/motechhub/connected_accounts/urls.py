from django.conf.urls import url
from connected_accounts import views

urlpatterns = [
    url('^$', views.ConnectedAccountsView.as_view()),
    url('^account/$', views.save_connected_account),
]
