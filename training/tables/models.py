from django.db import models
from verbs.models import Verb


class Table(models.Model):
    name = models.fields.CharField(
        max_length=30
    )
    verbs = models.ManyToManyField(
        Verb,
        through='TableVerb',
        related_name='tables'
    )
    default = models.fields.BooleanField(
        default=False
    )

    def __str__(self):
        return self.name


class TableVerb(models.Model):
    table = models.ForeignKey(
        to=Table,
        on_delete=models.CASCADE
    )
    verb = models.ForeignKey(
        to=Verb,
        on_delete=models.CASCADE
    )
    done = models.BooleanField(
        default=False
    )
    success = models.BooleanField(
        default=False
    )
