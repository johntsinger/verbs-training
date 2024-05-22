import uuid
from django.db import models


class Verb(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4
    )
    infinitive = models.CharField(
        max_length=50,
        blank=True
    )
    simple_past = models.CharField(
        max_length=50,
        blank=True
    )
    past_participle = models.CharField(
        max_length=50,
        blank=True
    )
    translation = models.CharField(
        max_length=50,
        blank=True
    )

    def __str__(self):
        return (
            f"{self.infinitive} {self.simple_past} "
            f"{self.past_participle} {self.translation}"
        )


class Example(models.Model):
    example = models.CharField(
        max_length=255
    )
    translation = models.CharField(
        max_length=255
    )
    verb = models.ForeignKey(
        to=Verb,
        on_delete=models.CASCADE,
        related_name="examples"
    )

    def __str__(self):
        return f"Example for verb {self.verb}"


class Group(models.Model):
    BASE = "BASE"
    FORM = "FORM"
    GROUP_TYPE_CHOICES = [
        (BASE, "Verb base"),
        (FORM, "Verb form")
    ]
    name = models.CharField(
        max_length=50,
        unique=True
    )
    group_type = models.CharField(
        max_length=4,
        choices=GROUP_TYPE_CHOICES
    )
    verbs = models.ManyToManyField(
        to=Verb,
        related_name="groups"
    )

    def __str__(self):
        return f"{self.name} - {self.group_type}"
