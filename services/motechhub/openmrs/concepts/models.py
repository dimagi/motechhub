from __future__ import unicode_literals
import json
from django.db import models
from openmrs.credentials.models import OpenmrsInstance
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class OpenmrsConcept(models.Model):
    uuid = models.CharField(max_length=256, primary_key=True)
    instance = models.ForeignKey(OpenmrsInstance)
    display = models.TextField()
    concept_class = models.CharField(max_length=256)
    retired = models.BooleanField()
    datatype = models.CharField(max_length=256)
    answers = models.ManyToManyField('OpenmrsConcept')
    descriptions = models.TextField(validators=(json.dumps,))
    names = models.TextField(validators=(json.dumps,))

    def __str__(self):
        return 'OpenMRS Concept {}: {}'.format(self.uuid, self.display)
