from django.conf.urls import url
from openmrs import views

urlpatterns = [
    url(r'^rest/(?P<credential_id>\d+)/concept/$',
        views.all_openmrs_concepts,
        name='all_openmrs_concepts'),
    url(r'^rest/concept/search/$',
        views.concept_search,
        name='openmrs_concept_search'),
    url(r'^concept/search/$',
        views.concept_search_page,
        name='openmrs_concept_search_page'),
]
