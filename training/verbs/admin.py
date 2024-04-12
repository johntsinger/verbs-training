from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from verbs.models import Verb


class VerbAdminForm(forms.ModelForm):
    class Meta:
        model = Verb
        fields = [
            'infinitive',
            'simple_past',
            'past_participle',
            'translation'
        ]

    def clean(self):
        """
        A Verb must have all fields filled to be saved.
        Can not be done in the model because Verb model
        requiers blank=True for exercise form.
        """
        errors = [
            key for key, value in self.cleaned_data.items() if not value
        ]
        if errors:
            raise ValidationError(
                {field: 'This field is required.' for field in errors}
            )


class VerbAdmin(admin.ModelAdmin):
    form = VerbAdminForm
    list_display = [
        'infinitive',
        'simple_past',
        'past_participle',
        'translation'
    ]
    ordering = ('infinitive',)


admin.site.register(Verb, VerbAdmin)
