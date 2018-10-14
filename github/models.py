from django.db import models


class Issue(models.Model):
    github_id = models.BigIntegerField()
    comments_count = models.IntegerField()
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

