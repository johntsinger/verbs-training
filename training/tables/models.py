import uuid
from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint
from django.core.exceptions import ValidationError
from verbs.models import Verb
from profiles.models import Profile


class Table(models.Model):
    DEFAULT_TABLE = "defaulttable"
    USER_TABLE = "usertable"

    CHOICES = [
        (DEFAULT_TABLE, "Default Table"),
        (USER_TABLE, "User Table")
    ]
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4
    )
    type = models.CharField(
        max_length=12,
        choices=CHOICES
    )
    name = models.fields.CharField(
        max_length=30,
    )
    verbs = models.ManyToManyField(
        to=Verb,
        related_name="tables"
    )
    owner = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        related_name="tables",
        null=True
    )
    is_available = models.BooleanField(
        default=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['name'],
                condition=Q(type="defaulttable"),
                name=(
                    'unique_default_table_name'
                )
            ),
            UniqueConstraint(
                fields=['name', 'owner'],
                condition=Q(type="usertable"),
                name=(
                    'unique_table_name_per_profile'
                )
            )
        ]

    def __str__(self):
        return f"{self.name}"


class DefaultTableManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(type="defaulttable")


class UserTableManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(type="usertable")


class DefaultTable(Table):
    objects = DefaultTableManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs) -> None:
        self.type = self.DEFAULT_TABLE
        self.owner = None
        return super().save(*args, **kwargs)

    def clean(self) -> None:
        if DefaultTable.objects.filter(
            name=self.name
        ).exclude(
            id=self.id
        ):
            raise ValidationError(
                "Default table with this Name already exists.",
            )
        return super().clean()


class UserTable(Table):
    objects = UserTableManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs) -> None:
        self.type = self.USER_TABLE
        return super().save(*args, **kwargs)

    def clean(self) -> None:
        if UserTable.objects.filter(
            name=self.name,
            owner=self.owner
        ).exclude(
            id=self.id
        ):
            raise ValidationError(
                "User table with this Name and Owner already exists.",
            )
        return super().clean()
