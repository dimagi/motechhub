from django.db import models


class CommcarehqInstance(models.Model):
    domain = models.CharField(max_length=256)
    url = models.URLField()
    commcarehq_domain = models.CharField(max_length=256)


class CommcarehqCredential(models.Model):
    instance = models.ForeignKey(CommcarehqInstance)
    username = models.EmailField()
    api_key = models.CharField(max_length=256)
