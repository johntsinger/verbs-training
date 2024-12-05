from itertools import groupby

from django.forms.models import (
    ModelChoiceField,
    ModelChoiceIterator,
    ModelMultipleChoiceField,
)


class OptGroupMixin:
    def __init__(
        self,
        queryset,
        group_by_field,
        group_label=None,
        *args,
        **kwargs,
    ):
        """
        - queryset (queryset): The queryset, must be order_by.
        - group_by_field (str): The name of a field on the model to
            use as an optgroup.
        - group_label (func default=None): A function to return a label
            for each optgroup.
        """
        super().__init__(queryset, *args, **kwargs)
        self.group_by_field = group_by_field
        if group_label is None:
            self.group_label = lambda group: group
        else:
            self.group_label = group_label

    def _get_choices(self):
        if hasattr(self, "_choices"):
            return self._choices
        return GroupedModelChoiceIterator(self)


class GroupedModelChoiceIterator(ModelChoiceIterator):
    """Yield grouped choices."""

    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)
        queryset = self.queryset.all()
        if not queryset._prefetch_related_lookups:
            queryset = queryset.iterator()
        for group, choices in groupby(
            self.queryset.all(),
            key=lambda table: getattr(table, self.field.group_by_field),
        ):
            yield (
                self.field.group_label(group) or "(Nameless)",
                [self.choice(choice) for choice in choices],
            )


class GroupedModelChoiceField(OptGroupMixin, ModelChoiceField):
    """Group for ModelChoiceField"""

    choices = property(OptGroupMixin._get_choices, ModelChoiceField.choices.fset)


class GroupedModelMultiChoiceField(OptGroupMixin, ModelMultipleChoiceField):
    """Group for ModelMultipleChoiceField"""

    # doesn't work with widget FilteredSelectMultiple
    choices = property(
        OptGroupMixin._get_choices, ModelMultipleChoiceField.choices.fset
    )
