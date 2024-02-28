from django.db import models
from django.db.models.constraints import UniqueConstraint
from verbs.models import Verb
from profiles.models import Profile


class AbstractTable(models.Model):
    name = models.fields.CharField(
        max_length=30
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class DefaultTable(AbstractTable):
    verbs = models.ManyToManyField(
        Verb,
        related_name='defaut_tables'
    )
    profile = None
    __original_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_name = self.name

    def save(self, *args, **kwargs):
        if self.pk:
            if self.__original_name != self.name:
                UserTable.objects.filter(
                    name=self.__original_name
                ).update(
                    name=self.name
                )
                self.__original_name = self.name
        else:
            user_tables = [
                UserTable(
                    name=self.name,
                    profile=profile
                )
                for profile in Profile.objects.all()
            ]
            UserTable.objects.bulk_create(user_tables)
        super().save(*args, **kwargs)


class UserTable(AbstractTable):
    verbs = models.ManyToManyField(
        Verb,
        through='TableVerb',
        related_name='user_tables'
    )
    profile = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        related_name='user_tables',
        blank=True,
        null=True
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['name', 'profile'],
                name='unique table name'
            )
        ]


class TableVerb(models.Model):
    table = models.ForeignKey(
        to=UserTable,
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
