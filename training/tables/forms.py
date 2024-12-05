from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.exceptions import ValidationError
from django.forms import formset_factory
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from training.tables.models import DefaultTable, Table, UserTable
from training.verbs.models import Verb


class TableForm(forms.ModelForm):
    """Base Table model form."""

    name = forms.CharField(
        label=_("Name"),
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "onfocus": "moveCursorOnFocus(this)",
                "autocomplete": "name",
            }
        ),
        help_text=_("Required. The name of the table"),
    )

    verbs = forms.ModelMultipleChoiceField(
        queryset=Verb.objects.all(),
        required=True,
        widget=FilteredSelectMultiple(
            verbose_name="Verbs",
            is_stacked=False,
        ),
    )

    # Minimun number of verbs in verbs m2m.
    min_num_verbs = 10

    class Media:
        extend = True
        css = {"all": ("admin/css/widgets.css",)}

    class Meta:
        fields = ("name", "verbs")
        model = Table

    def clean(self):
        verbs = self.cleaned_data.get("verbs", self.Meta.model.objects.none())
        verbs_count = verbs.count()
        if verbs_count < self.min_num_verbs:
            raise self.get_min_number_verbs_error(verbs_count)
        return super().clean()

    def get_min_number_verbs_error(self, verbs_count):
        return ValidationError(
            gettext(
                "Please select at least %(min_num_verbs)s "
                "verbs to create a table. "
                "(%(total_missing)s missing verbs)"
            ),
            code="min_number_verbs",
            params={
                "total_missing": self.min_num_verbs - verbs_count,
                "min_num_verbs": self.min_num_verbs,
            },
        )


class DefaultTableForm(TableForm):
    class Meta(TableForm.Meta):
        model = DefaultTable

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if (
            self.Meta.model.objects.filter(name=name)
            .exclude(id=self.instance.id)
            .exists()
        ):
            raise ValidationError(
                gettext("A default table with this Name already exists."),
                code="unique_name",
            )
        return name


class UserTableForm(TableForm):
    # Maximum number of UserTables per user.
    max_per_user = 10

    class Meta(TableForm.Meta):
        model = UserTable

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop("owner", None)
        super().__init__(*args, **kwargs)
        if owner:
            self.instance.owner = owner

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if (
            self.Meta.model.objects.filter(
                name__iexact=name,
                owner=self.instance.owner,
            )
            .exclude(id=self.instance.id)
            .exists()
        ):
            raise ValidationError(
                gettext("You already have a Table with this Name."), code="unique_name"
            )
        return name

    def clean(self):
        owner = self.instance.owner
        # Prevent user having more that 10 UserTable objects
        if self.Meta.model.objects.filter(owner=owner).count() >= self.max_per_user:
            raise ValidationError(
                gettext(
                    "Maximum number of user tables reached. "
                    "(%(max_per_user)s of %(max_per_user)s)"
                ),
                code="max_per_user",
                params={"max_per_user": self.max_per_user},
            )
        return super().clean()


class TrainingForm(forms.Form):
    infinitive = forms.CharField(
        label=_("Infinitive"),
        required=False,
    )
    simple_past = forms.CharField(
        label=_("Simple past"),
        required=False,
    )
    past_participle = forms.CharField(
        label=_("Past participle"),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.field_template = "bootstrap5/layout/inline_field.html"
        self.helper.layout = Layout(
            "infinitive",
            "simple_past",
            "past_participle",
        )

    def clean_infinitive(self):
        return self.cleaned_data.get("infinitive").lower()

    def clean_simple_past(self):
        return self.cleaned_data.get("simple_past").lower()

    def clean_past_participle(self):
        return self.cleaned_data.get("past_participle").lower()


VerbFormSet = formset_factory(
    TrainingForm,
    extra=0,
)
