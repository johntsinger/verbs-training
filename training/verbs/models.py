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
        max_length=70,
    )
    simple_past = models.CharField(
        max_length=70,
    )
    past_participle = models.CharField(
        max_length=70,
    )
    translation = models.CharField(
        max_length=70,
    )
    similarity = models.ForeignKey(
        to='Similarity',
        on_delete=models.PROTECT,
        related_name='verbs',
        null=True
    )

    def __str__(self) -> str:
        return (
            f'{self.infinitive} {self.simple_past} '
            f'{self.past_participle} {self.translation}'
        )


class Info(models.Model):
    content = models.CharField(
        max_length=255
    )
    verb = models.ForeignKey(
        to=Verb,
        on_delete=models.CASCADE,
        related_name='info'
    )

    def __str__(self) -> str:
        return f'Info for verb {self.verb.infinitive}'


class Example(models.Model):
    english = models.CharField(
        max_length=255
    )
    translation = models.CharField(
        max_length=255
    )
    verb = models.ForeignKey(
        to=Verb,
        on_delete=models.CASCADE,
        related_name='examples'
    )

    def __str__(self) -> str:
        return f'Example for verb {self.verb.infinitive}'


class Similarity(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name_plural = 'Similarities'

    def __str__(self) -> str:
        return f'{self.name}'
