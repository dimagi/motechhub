from __future__ import unicode_literals
from django.db import models


class OpenmrsInstance(models.Model):
    domain = models.CharField(max_length=256)
    name = models.TextField()
    url = models.URLField()


class OpenmrsCredential(models.Model):
    instance = models.ForeignKey(OpenmrsInstance)
    username = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
