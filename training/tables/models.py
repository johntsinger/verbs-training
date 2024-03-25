import uuid
from django.db import models
from django.db.models.constraints import UniqueConstraint
from verbs.models import Verb
from profiles.models import Profile


class AbstractTable(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4
    )
    name = models.fields.CharField(
        max_length=30
    )
    verbs = models.ManyToManyField(
        to=Verb,
        related_name='%(class)s'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class DefaultTable(AbstractTable):
    is_available = models.BooleanField(
        default=True
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['name'],
                name=(
                    '%(app_label)s_%(class)s_'
                    'unique_name'
                )
            )
        ]


class UserTable(AbstractTable):
    profile = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        related_name='usertables'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['name', 'profile'],
                name=(
                    '%(app_label)s_%(class)s_'
                    'unique_name_per_profile'
                )
            )
        ]


"""
def save(self, *args, **kwargs):
        # self._state.adding --> True (creation) or False (update)
        # Better than self.pk is None.
        created = self._state.adding
        super().save(*args, **kwargs)
        if created:
            self.profiles.set(
                Profile.objects.all()
            )
"""
