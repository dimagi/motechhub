from __future__ import unicode_literals
from django.db import models
from openmrs.credentials.models import OpenmrsInstance


class OpenmrsConcept(models.Model):
    instance = models.ForeignKey(OpenmrsInstance)
    display = models.TextField()
    uuid = models.CharField()
