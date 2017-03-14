from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField
from streams.models import Stream


class Job(models.Model):
    stream = models.ForeignKey(Stream)
    javascript = models.TextField()
    filter = JSONField()
