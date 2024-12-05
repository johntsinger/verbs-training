import uuid

from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint
from django.db.models.functions import Lower
from django.utils.text import slugify

from training.profiles.models import Profile
from training.verbs.models import Verb


class Table(models.Model):
    DEFAULT_TABLE = "defaulttable"
    USER_TABLE = "usertable"

    CHOICES = [
        (DEFAULT_TABLE, "Default Table"),
        (USER_TABLE, "User Table"),
    ]
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )
    type = models.CharField(
        max_length=12,
        choices=CHOICES,
    )
    name = models.CharField(
        max_length=30,
    )
    slug_name = models.SlugField()
    verbs = models.ManyToManyField(
        to=Verb,
        related_name="tables",
    )
    owner = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        related_name="tables",
        null=True,
    )
    is_available = models.BooleanField(
        default=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower("name"),
                condition=Q(
                    type="defaulttable",
                ),
                name=("unique_default_table_name"),
            ),
            UniqueConstraint(
                Lower("name"),
                "owner",
                condition=Q(type="usertable"),
                name=("unique_table_name_per_profile"),
            ),
        ]

    def save(self, *args, **kwargs):
        self.slug_name = slugify(self.name)
        # self.clean()
        return super().save(*args, **kwargs)

    def get_verbs_success(self):
        return [verb for verb in self.verbs.all() if verb.is_success is True]

    def get_verbs_unsuccess(self):
        return [verb for verb in self.verbs.all() if verb.is_success is False]

    def get_verbs_not_done(self):
        return [verb for verb in self.verbs.all() if verb.is_success is None]

    def resolve_proxy_model(self):
        """Get the proxy model."""
        if self.type == self.DEFAULT_TABLE:
            self.__class__ = DefaultTable
        else:
            self.__class__ = UserTable
        return self

    def __str__(self):
        return f"{self.name}"


class DefaultTableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.DEFAULT_TABLE)


class UserTableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.USER_TABLE)


class DefaultTable(Table):
    objects = DefaultTableManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.type = self.DEFAULT_TABLE
        self.owner = None
        return super().save(*args, **kwargs)


class UserTable(Table):
    objects = UserTableManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.type = self.USER_TABLE
        return super().save(*args, **kwargs)

    # def clean(self):
    #     # UserTable must have an owner.
    #     if not self.owner:
    #         raise ValueError(
    #             {
    #                 'owner':
    #                 'UserTable must have an owner.'
    #             }
    #         )
    #     return super().clean()
