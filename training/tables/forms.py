from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

from django import forms
from django.forms import formset_factory
from django.utils.translation import gettext_lazy as _


class TrainingForm(forms.Form):
    infinitive = forms.CharField(
        label=_('Infinitive'),
        required=False
    )
    simple_past = forms.CharField(
        label=_('Simple past'),
        required=False
    )
    past_participle = forms.CharField(
        label=_('Past participle'),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.field_template = 'bootstrap5/layout/inline_field.html'
        self.helper.layout = Layout(
            'infinitive',
            'simple_past',
            'past_participle',
        )

    def clean_infinitive(self):
        return self.cleaned_data.get('infinitive').lower()

    def clean_simple_past(self):
        return self.cleaned_data.get('simple_past').lower()

    def clean_past_participle(self):
        return self.cleaned_data.get('past_participle').lower()


VerbFormSet = formset_factory(
    TrainingForm,
    extra=0,
)
