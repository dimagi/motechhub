"""motechrunner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from jobs.views import handle_job, get_job_list
from motechmessages.views import _post_message, handle_messages
from streams.views import list_streams, handle_stream

uuid_re = r'[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}'

urlpatterns = [
    url(r'^_admin/', admin.site.urls),
    url(r'^$', list_streams),
    url(r'^(?P<stream_name>[a-z-]+)$', handle_stream),
    url(r'^(?P<stream_name>[a-z-]+)/job$', get_job_list),
    url(r'^(?P<stream_name>[a-z-]+)/job/(?P<job_id>{})$'.format(uuid_re), handle_job),
    url(r'^(?P<stream_name>[a-z-]+)/message$', handle_messages),
]
