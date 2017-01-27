from commcarehq.restclient.listapi import CommcarehqListApi


def get_applications(credential):
    api = CommcarehqListApi(credential, 'application')
    return [{'app_id': app['id'], 'name': app['name']} for app in api.get_all()]


def get_application_forms(credential, app_id):
    api = CommcarehqListApi(credential, 'application')
    matching_apps = [app for app in api.get_all() if app['id'] == app_id]
    if matching_apps:
        app, = matching_apps

        return [
            {'xmlns': form['xmlns'], 'name': form['name'], 'id': form['unique_id']}
            for module in app['modules'] for form in module['forms']]
    else:
        return []


def get_application_form_questions(credential, app_id, form_id):
    api = CommcarehqListApi(credential, 'application')
    matching_apps = [app for app in api.get_all() if app['id'] == app_id]
    if matching_apps:
        app, = matching_apps
        matching_forms = [
            form for module in app['modules'] for form in module['forms']
            if form['unique_id'] == form_id]
        if matching_forms:
            form, = matching_forms
            return form['questions']
        return
    else:
        return []
