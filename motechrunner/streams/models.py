from __future__ import unicode_literals

from django.db import models


class Stream(models.Model):
    name = models.CharField(max_length=255)
