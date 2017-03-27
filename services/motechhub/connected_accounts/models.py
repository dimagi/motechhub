from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField

from django.db import models


class ConnectedAccount(models.Model):
    domain = models.CharField(max_length=255, db_index=True)
    token = models.UUIDField(unique=True)
    token_password = models.BinaryField(max_length=16)  # 128 bit key
    account_type = models.CharField(max_length=32)
    account_info = JSONField()
