from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms
from tables.models import Table, TableVerb
from verbs.models import Verb


class TableAdminForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['name', 'verbs', 'default']

    verbs = forms.ModelMultipleChoiceField(
        queryset=Verb.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Verbs',
            is_stacked=False
        )
    )

    def __init__(self, *args, **kwargs):
        super(TableAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['verbs'].initial = self.instance.verbs.all()

    def save(self, commit=True):
        table = super(TableAdminForm, self).save(commit=False)
        if commit:
            table.save()

        if table.pk:
            table.verbs = self.cleaned_data['verbs']
            self.save_m2m()

        return table


class TableAdmin(admin.ModelAdmin):
    form = TableAdminForm
    list_display = [
        'name',
        'default'
    ]
    ordering = ('name',)


class TableVerbAdmin(admin.ModelAdmin):
    list_display = [
        'table',
        'verb',
    ]
    ordering = ('table__name', 'verb')


admin.site.register(Table, TableAdmin)
admin.site.register(TableVerb, TableVerbAdmin)
