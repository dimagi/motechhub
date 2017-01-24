from django.conf.urls import url
from openmrs import views

urlpatterns = [
    url(r'^rest/(?P<credential_id>\d+)/concept/',
        views.all_openmrs_concepts,
        name='all_openmrs_concepts'),
]
