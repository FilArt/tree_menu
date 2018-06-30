from django.db import models
from django.contrib.postgres.fields import JSONField


class Menu(models.Model):
    name = models.CharField(max_length=30)
    nodes = JSONField()

    def __str__(self):
        return self.name
