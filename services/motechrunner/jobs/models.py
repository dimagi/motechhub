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

    @classmethod
    def get_latest_jobs(cls, stream):
        return cls.objects.raw("""
          SELECT * FROM jobs_job AS job INNER JOIN (
            SELECT job.uuid, MAX(job.rev) AS rev
            FROM jobs_job as job
            WHERE stream_id = %(stream_id)s
            GROUP BY job.uuid
          ) job_inner
          ON stream_id = %(stream_id)s AND job.rev = job_inner.rev AND job.uuid = job_inner.uuid
          ORDER BY job.modified
        """, {'stream_id': stream.id})

    def save(self, *args, **kwargs):
        if self.pk:
            raise ReadOnlyError(
                'The Job table is append only. '
                'To "edit" a row, create a new row with an incremented rev.')
        super(Job, self).save(*args, **kwargs)
