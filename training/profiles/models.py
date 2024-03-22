from django.db import models
from django.contrib.auth import get_user_model
from verbs.models import Verb


User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE
    )
    default_tables = models.ManyToManyField(
        to='tables.DefaultTable',
        related_name='profiles'
    )

    def __str__(self):
        return self.user.username


class Result(models.Model):
    profile = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        related_name='results'
    )
    verb = models.ForeignKey(
        to=Verb,
        on_delete=models.CASCADE,
        related_name='results'
    )
    table = models.ForeignKey(
        to='tables.UserTable',
        on_delete=models.CASCADE,
        related_name='results',
        null=True,
        blank=True,
    )
    default_table = models.ForeignKey(
        to='tables.DefaultTable',
        on_delete=models.CASCADE,
        related_name='results',
        null=True,
        blank=True,
    )
    done = models.BooleanField(
        default=False
    )
    success = models.BooleanField(
        default=False
    )
