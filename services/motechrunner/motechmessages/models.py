from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField
from streams.models import Stream


class Message(models.Model):
    stream = models.ForeignKey(Stream)
    uuid = models.UUIDField()
    body = JSONField()
    created = models.DateTimeField(auto_now=True)


class MessageRun(models.Model):
    message = models.ForeignKey(Message)
    state = models.CharField(
        max_length=9,
        choices=(
            ('scheduled', 'Scheduled'),
            ('started', 'Started'),
            ('success', 'Success'),
            ('failed', 'Failed'),
        )
    )


class MessageRunArtifact(models.Model):
    message_run = models.ForeignKey(MessageRun)
    created = models.DateTimeField(auto_now=True)
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
