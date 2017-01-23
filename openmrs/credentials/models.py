from __future__ import unicode_literals
from django.db import models


class OpenmrsInstance(models.Model):
    domain = models.CharField()
    name = models.TextField()
    url = models.URLField()


class OpenmrsCredential(models.Model):
    instance = models.ForeignKey(OpenmrsInstance)
    username = models.CharField()
    password = models.CharField()
