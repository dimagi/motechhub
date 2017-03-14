from django.shortcuts import render


def step_0_start(request, domain):
    return render(request, 'prototype/step_0_start.html', {'domain': domain})


def step_1_trigger_commcarehq(request, domain):
    return render(request, 'prototype/step_1_trigger_commcarehq.html', {'domain': domain})


def step_2_select_form(request, domain):
    return render(request, 'prototype/step_2_select_form.html', {'domain': domain})


def step_3_select_action(request, domain):
    return render(request, 'prototype/step_3_select_action.html', {'domain': domain})


def step_4_action_openmrs(request, domain):
    return render(request, 'prototype/step_4_action_openmrs.html', {'domain': domain})


def step_5_select_encounter_type(request, domain):
    return render(request, 'prototype/step_5_select_encounter_type.html', {'domain': domain})


def step_6_configure_encounter_action(request, domain):
    return render(request, 'prototype/step_6_configure_encounter_action.html', {'domain': domain})
