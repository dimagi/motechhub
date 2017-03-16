from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField
from streams.models import Stream


class Message(models.Model):
    stream = models.ForeignKey(Stream)
    body = JSONField()


class MessageRunState(object):
    scheduled = 0
    started = 1
    success = 2
    failed = 3


class MessageRun(models.Model):
    message = models.ForeignKey(Message)
    state = models.IntegerField()


class MessageRunArtifact(models.Model):
    message_run = models.ForeignKey(MessageRun)
    created = models.DateTimeField(auto_now=True)
    level = models.CharField(
        max_length=5,
        choices=(('DEBUG', 'Debug'), ('INFO', 'Info'),
                 ('WARN', 'Warn'), ('ERROR', 'Error')))
    body = JSONField()
