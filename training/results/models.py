import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.constraints import UniqueConstraint

from training.profiles.models import Profile
from training.tables.models import Table
from training.verbs.models import Verb


class ResultManager(models.Manager):
    def create(self, *, owner, table, verb, **kwargs):
        if not owner:
            raise ValueError("Result must have an owner")
        if not table:
            raise ValueError("Result must have a table")
        if not verb:
            raise ValueError("Result must have a verb")
        return super().create(owner=owner, table=table, verb=verb, **kwargs)


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
    owner = models.ForeignKey(
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

    objects = ResultManager()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=[
                    "owner",
                    "table",
                    "verb",
                ],
                name="unique_result_for_verb_in_table_per_owner",
            )
        ]

    def clean(self):
        if not self.table.verbs.filter(id=self.verb.id).exists():
            raise ValidationError(
                {
                    "verb": (
                        f"The verb '{self.verb}' does not belong to "
                        f"'{self.table}' table."
                    )
                }
            )
        if self.table.owner and self.table.owner.id != self.owner.id:
            raise ValidationError(
                {
                    "table": (
                        f"The table '{self.table}' does not belong to "
                        f"'{self.owner} profile"
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return (
            "Result: "
            f"owner <{self.owner}> "
            f"table <{self.table}> "
            f"verb <{self.verb.infinitive}>"
        )
