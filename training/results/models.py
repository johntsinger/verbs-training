import uuid
from django.db import models
from django.db.models import Q
from django.db.models.constraints import CheckConstraint
from verbs.models import Verb
from profiles.models import Profile
from tables.models import DefaultTable, UserTable


class Result(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4
    )
    verb = models.ForeignKey(
        to=Verb,
        on_delete=models.CASCADE,
        related_name='results'
    )
    profile = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        related_name='results'
    )
    default_table = models.ForeignKey(
        to=DefaultTable,
        on_delete=models.CASCADE,
        related_name='results',
        null=True,
        blank=True
    )
    user_table = models.ForeignKey(
        to=UserTable,
        on_delete=models.CASCADE,
        related_name='results',
        null=True,
        blank=True
    )
    is_success = models.BooleanField(
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            CheckConstraint(
                check=(
                    Q(default_table__isnull=True)
                    ^ Q(user_table__isnull=True)
                ),
                name=(
                    '%(app_label)s_%(class)s_'
                    'only_default_table_or_user_table_must_be_set'
                )
            )
        ]

    @property
    def table(self):
        return self.default_table or self.user_table
        """
        if self.default_table and self.user_table:
            raise AssertionError(
                "Both 'default_table' and 'usertables' are set."
            )
        elif self.default_table:
            return self.default_table
        elif self.user_table:
            return self.user_table
        else:
            raise AssertionError(
                "Neither 'default_table' nor 'user_table' is set."
            )
        """
