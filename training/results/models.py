import uuid
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.constraints import UniqueConstraint
from verbs.models import Verb
from profiles.models import Profile
from tables.models import Table


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
    table = models.ForeignKey(
        to=Table,
        on_delete=models.CASCADE,
        related_name='results',
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
            UniqueConstraint(
                fields=["verb", "profile", "table"],
                name="unique_result_for_verb_in_table_per_profile"
            )
        ]

    def clean(self):
        if (
            hasattr(self, 'table')
            and not self.table.verbs.filter(id=self.verb_id)
        ):
            raise ValidationError(
                {
                    "verb": "Verb must belong to table."
                }
            )

        if (
            hasattr(self, 'table')
            and hasattr(self, 'profile')
            and self.table.owner
            and self.table.owner != self.profile
        ):
            raise ValidationError(
                {
                    "table": "Table must belong to profile"
                }
            )

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
