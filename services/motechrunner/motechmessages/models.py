from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField
from jobs.models import Job
from shared.django_models.append_only import AppendOnlyModelMixin
from streams.models import Stream


class Message(AppendOnlyModelMixin, models.Model):
    """
    Incoming message body and meta data

    A message's row is not touched once it is written,
    all tracking is done in the other models

    """
    stream = models.ForeignKey(Stream)
    uuid = models.UUIDField()
    body = JSONField()
    created = models.DateTimeField(auto_now_add=True)


class MessageRun(AppendOnlyModelMixin, models.Model):
    """
    An attempt to run a message, which may include running multiple jobs on it

    A message can fail and be retried. Each attempt
    (either the original one or user-triggered retry)
    is recorded as a MessageRun

    """
    message = models.ForeignKey(Message)
    created = models.DateTimeField(auto_now_add=True)


class MessageRunJob(models.Model):
    """
    Each MessageRun consists of 0 or more MessageRunJobs

    MessageRunJobs represent a run of a particular job on a message

    Messages that match no jobs will have a MessageRun with no MessageRunJobs.
    """
    message_run = models.ForeignKey(MessageRun)
    job = models.ForeignKey(Job)
    state = models.CharField(
        max_length=9,
        choices=(
            ('scheduled', 'Scheduled'),
            ('started', 'Started'),
            ('success', 'Success'),
            ('failed', 'Failed'),
        )
    )
    modified = models.DateTimeField(auto_now=True)


class MessageRunJobArtifact(AppendOnlyModelMixin, models.Model):
    """
    Each MessageRunJob will leave a series of MessageRunJobArtifacts

    These are like logging messages, where the log body is JSON.

    DEBUG artifacts will not be saved in production
    INFO artifacts let a run job communicate checkpoints and side effects achieved
    WARN artifacts indicate that the job detected abnormalities but ran to completion
    ERROR artifacts indicate that the job terminated unexpectedly

    """
    message_run = models.ForeignKey(MessageRunJob)
    created = models.DateTimeField(auto_now_add=True)
    level = models.CharField(
        max_length=5,
        choices=(
            ('DEBUG', 'Debug'),
            ('INFO', 'Info'),
            ('WARN', 'Warn'),
            ('ERROR', 'Error')
        )
    )
    body = JSONField()
