from django.db import models


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

    def __str__(self):
        return (
            f'{self.infinitive} {self.simple_past} '
            f'{self.past_participle} {self.translation}'
        )
