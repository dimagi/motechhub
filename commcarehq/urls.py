from django.conf.urls import url
from commcarehq import views

urlpatterns = [
    url(r'^rest/application/$',
        views.applications,
        name='commcarehq_applications'),
    url(r'^rest/application/(?P<app_id>(\w+))/form/$',
        views.application_forms,
        name='commcarehq_application_forms'),
    url(r'^rest/application/(?P<app_id>(\w+))/form/(?P<form_id>(\w+))/question/$',
        views.application_form_questions,
        name='commcarehq_application_form_questions'),
    url(r'^rest/case_properties/$',
        views.known_case_properties,
        name='commcarehq_known_case_properties'),
    url(r'^case_properties/$',
        views.known_case_properties_page,
        name='known_case_properties_page'),
]
