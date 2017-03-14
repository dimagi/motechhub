from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^start/', views.step_0_start, name='prototype_start'),
    url(r'^b1946ac/1/', views.step_1_trigger_commcarehq, name='prototype_trigger_commcarehq'),
    url(r'^b1946ac/2/', views.step_2_select_form, name='prototype_select_form'),
    url(r'^b1946ac/3/', views.step_3_select_action, name='prototype_select_action'),
    url(r'^b1946ac/4/', views.step_4_action_openmrs, name='prototype_action_openmrs'),
    url(r'^b1946ac/5/', views.step_5_select_encounter_type, name='step_5_select_encounter_type'),
    url(r'^b1946ac/6/', views.step_6_configure_encounter_action, name='step_6_configure_encounter_action'),
]
