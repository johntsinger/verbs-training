from django.apps import apps
from django.db import models
from django.db.models import OuterRef, Subquery


class VerbManager(models.Manager):
    _table_model = None

    @property
    def table_model(self):
        """Cache Table model"""
        if self._table_model is None:
            self._table_model = apps.get_model("tables.Table")
        return self._table_model

    def get_queryset_annotated(self, user, table):
        results_subquery = self._get_results_subquery(user=user, table=table)
        return (
            self.get_queryset()
            .annotate(is_success=Subquery(results_subquery))
            .distinct()
        )

    def _get_results_subquery(self, user, table):
        Result = apps.get_model("results.Result")
        return Result.objects.filter(
            owner=user.profile,
            table=table,
            verb=OuterRef("pk"),
        ).values("is_success")[:1]

    def _get_table(self, table):
        """Validate table argument."""
        instance = getattr(self, "instance", None)
        # if table argument is not provided the manager must be
        # attached to a Table instance
        if table is None:
            if not isinstance(instance, self.table_model):
                raise TypeError(
                    "The 'table' argument must be provided when the manager "
                    "is not attached to a Table instance."
                )
            return instance
        if isinstance(table, self.table_model) and isinstance(
            instance, self.table_model
        ):
            raise TypeError(
                "The 'table' argument must be None when the manager is "
                "attached to a Table instance."
            )
        return table

    def _user_owns_table(self, user, table):
        """Ensure that user owns the table if it's a UserTable."""
        if table.owner is not None and user.profile != table.owner:
            raise PermissionError("This user does not have access to this table.")

    def with_results(self, *, user, table=None):
        table = self._get_table(table)
        # When the table argument is an OuterRef object (views),
        # it cannot be directly used to filter the queryset.
        if isinstance(table, self.table_model):
            self._user_owns_table(user, table)
            return self.get_queryset_annotated(user=user, table=table).filter(
                tables=table
            )
        return self.get_queryset_annotated(user=user, table=table)


class Verb(models.Model):
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
        to="Similarity",
        on_delete=models.PROTECT,
        related_name="verbs",
        null=True,
    )

    objects = VerbManager()

    class Meta:
        ordering = [
            "infinitive",
        ]

    def __str__(self) -> str:
        return (
            f"{self.infinitive} {self.simple_past} "
            f"{self.past_participle} {self.translation}"
        )


class Info(models.Model):
    content = models.CharField(
        max_length=255,
    )
    verb = models.ForeignKey(
        to=Verb,
        on_delete=models.CASCADE,
        related_name="info",
    )

    def __str__(self) -> str:
        return f"Info for verb {self.verb.infinitive}"


class Example(models.Model):
    english = models.CharField(
        max_length=255,
    )
    translation = models.CharField(
        max_length=255,
    )
    verb = models.ForeignKey(
        to=Verb,
        on_delete=models.CASCADE,
        related_name="examples",
    )

    def __str__(self) -> str:
        return f"Example for verb {self.verb.infinitive}"


class Similarity(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    class Meta:
        verbose_name_plural = "Similarities"

    def __str__(self) -> str:
        return f"{self.name}"
