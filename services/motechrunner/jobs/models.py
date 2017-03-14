from __future__ import unicode_literals
from django.core.validators import MinValueValidator

from django.db import models
from jsonfield import JSONField
from jobs.exceptions import ReadOnlyError
from streams.models import Stream


class Job(models.Model):
    uuid = models.UUIDField()
    rev = models.PositiveIntegerField(validators=MinValueValidator(1))
    stream = models.ForeignKey(Stream)
    javascript = models.TextField()
    filter = JSONField()
    modified = models.DateTimeField(auto_now=True)

    class Meta(object):
        unique_together = ('uuid', 'rev')
        index_together = ('stream', 'uuid', 'rev')

    def save(self, *args, **kwargs):
        if self.pk:
            raise ReadOnlyError(
                'The Job table is append only. '
                'To "edit" a row, create a new row with an incremented rev.')
        super(Job, self).save(*args, **kwargs)
