from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms
from tables.models import (
    DefaultTable,
    UserTable,
    TableVerb
)
from verbs.models import Verb


class TableAdminFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['verbs'].initial = self.instance.verbs.all()


class DefaultTableAdminForm(TableAdminFormMixin, forms.ModelForm):
    class Meta:
        model = DefaultTable
        fields = [
            'name',
            'verbs',
        ]

    verbs = forms.ModelMultipleChoiceField(
        queryset=Verb.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Verbs',
            is_stacked=False
        )
    )


class UserTableAdminForm(TableAdminFormMixin, forms.ModelForm):
    class Meta:
        model = UserTable
        fields = [
            'name',
            'profile',
            'verbs',
        ]

    verbs = forms.ModelMultipleChoiceField(
        queryset=Verb.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Verbs',
            is_stacked=False
        )
    )


class DefaultTableAdmin(admin.ModelAdmin):
    form = DefaultTableAdminForm
    list_display = [
        'name',
    ]
    ordering = ('name',)


class UserTableAdmin(admin.ModelAdmin):
    form = UserTableAdminForm
    list_display = [
        'name',
        'profile',
    ]
    ordering = ('name',)


class TableVerbAdmin(admin.ModelAdmin):
    list_display = [
        'get_user',
        'table',
        'verb',
    ]
    ordering = (
        'table__profile__user__username',
        'table__name',
        'verb'
    )

    @admin.display(
        ordering='table__profile',
        description='User'
    )
    def get_user(self, obj):
        return obj.table.profile


admin.site.register(DefaultTable, DefaultTableAdmin)
admin.site.register(UserTable, UserTableAdmin)
admin.site.register(TableVerb, TableVerbAdmin)
