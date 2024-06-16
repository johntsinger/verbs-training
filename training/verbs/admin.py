from django import forms
from django.db import models
from django.contrib import admin
from django.core.exceptions import ValidationError
from verbs.models import Verb, Info, Example


class InfoInline(admin.StackedInline):
    model = Info
    extra = 0
    formfield_overrides = {
        models.CharField: {
            'widget': forms.TextInput(attrs={"size": "100"})
        },
    }


class ExampleInline(admin.StackedInline):
    model = Example
    extra = 0
    formfield_overrides = {
        models.CharField: {
            'widget': forms.TextInput(attrs={"size": "100"})
        },
    }


class VerbAdminForm(forms.ModelForm):
    class Meta:
        model = Verb
        fields = [
            'infinitive',
            'simple_past',
            'past_participle',
            'translation',
            'similarity',
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
        'translation',
        'similarity',
    ]
    inlines = [
        InfoInline,
        ExampleInline
    ]
    ordering = ('infinitive',)


class InfoAdmin(admin.ModelAdmin):
    list_display = [
        "get_verb",
        "content"
    ]
    ordering = ('verb',)

    def get_verb(self, obj):
        return obj.verb.infinitive


class ExampleAdmin(admin.ModelAdmin):
    list_display = [
        "get_verb",
        "english",
        "translation"
    ]
    ordering = ('verb',)

    def get_verb(self, obj):
        return obj.verb.infinitive


admin.site.register(Verb, VerbAdmin)
admin.site.register(Info, InfoAdmin)
admin.site.register(Example, ExampleAdmin)
