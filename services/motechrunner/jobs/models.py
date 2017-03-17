from __future__ import unicode_literals
from django.core.validators import MinValueValidator

from django.db import models
from jsonfield import JSONField
from shared.django_models.append_only import AppendOnlyModelMixin
from streams.models import Stream


class Job(AppendOnlyModelMixin, models.Model):
    uuid = models.UUIDField()
    rev = models.PositiveIntegerField(validators=MinValueValidator(1))
    stream = models.ForeignKey(Stream)
    javascript = models.TextField()
    filter = JSONField()
    modified = models.DateTimeField(auto_now=True)

    class Meta(object):
        unique_together = ('uuid', 'rev')
        index_together = ('stream', 'uuid', 'rev')
