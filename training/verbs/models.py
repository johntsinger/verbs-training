from django.db import models


class VerbGroup(models.Model):
    name = models.CharField(
        max_length=50
    )


class Verb(models.Model):
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
    group = models.ForeignKey(
        to=VerbGroup,
        on_delete=models.SET_NULL,
        related_name='verbs',
        null=True
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
