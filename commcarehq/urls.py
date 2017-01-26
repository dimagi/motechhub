from django.conf.urls import url
from commcarehq import views

urlpatterns = [
    url(r'^rest/case_properties/$',
        views.known_case_properties,
        name='known_case_properties'),
    url(r'^case_properties/$',
        views.known_case_properties_page,
        name='known_case_properties_page'),
]
