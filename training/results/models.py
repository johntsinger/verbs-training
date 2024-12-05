import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.constraints import UniqueConstraint

from training.profiles.models import Profile
from training.tables.models import Table
from training.verbs.models import Verb


class Result(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )
    verb = models.ForeignKey(
        to=Verb,
        on_delete=models.CASCADE,
        related_name="results",
    )
    profile = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        related_name="results",
    )
    table = models.ForeignKey(
        to=Table,
        on_delete=models.CASCADE,
        related_name="results",
    )
    is_success = models.BooleanField(
        default=False,
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
                fields=[
                    "profile",
                    "table",
                    "verb",
                ],
                name="unique_result_for_verb_in_table_per_profile",
            )
        ]

    def clean(self):
        if (
            getattr(self, "table", None)
            and getattr(self, "verb", None)
            and not self.table.verbs.filter(id=self.verb_id)
        ):
            raise ValidationError({"verb": "Verb must belong to table."})

        if (
            getattr(self, "table", None)
            and getattr(self, "profile", None)
            and self.table.owner
            and self.table.owner != self.profile
        ):
            raise ValidationError({"table": "Table must belong to profile"})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            "Result: "
            f"user <{self.profile}> "
            f"table <{self.table}> "
            f"verb <{self.verb.infinitive}>"
        )
