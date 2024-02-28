from django.db import models
from django.contrib.auth import get_user_model
from verbs.models import Verb


User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE
    )
    verbs = models.ManyToManyField(
        to=Verb,
        through='UserVerb',
        related_name='profiles'
    )

    def __str__(self):
        return self.user.username


class UserVerb(models.Model):
    profile = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
    )
    verb = models.ForeignKey(
        to=Verb,
        on_delete=models.CASCADE,
    )
    done = models.BooleanField(
        default=False
    )
    success = models.BooleanField(
        default=False
    )
