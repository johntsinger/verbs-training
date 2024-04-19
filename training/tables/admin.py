from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms
from common.admin.mixins import GetReadOnlyFieldsMixin
from tables.models import (
    DefaultTable,
    UserTable,
)
from verbs.models import Verb


class TableAdminFormMixin:
    """
    Mixin to set initial verbs in tables change form.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['verbs'].initial = self.instance.verbs.all()


class DefaultTableAdminForm(
    TableAdminFormMixin,
    forms.ModelForm
):
    class Meta:
        model = DefaultTable
        fields = [
            'name',
            'verbs',
            'is_available'
        ]

    verbs = forms.ModelMultipleChoiceField(
        queryset=Verb.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Verbs',
            is_stacked=False
        )
    )


class UserTableAdminForm(
    TableAdminFormMixin,
    forms.ModelForm
):
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


class DefaultTableAdmin(
    GetReadOnlyFieldsMixin,
    admin.ModelAdmin
):
    form = DefaultTableAdminForm
    list_display = [
        'name',
    ]
    readonly_fields = (
        'created_at',
        'updated_at'
    )
    ordering = ('name',)


class UserTableAdmin(
    GetReadOnlyFieldsMixin,
    admin.ModelAdmin
):
    form = UserTableAdminForm
    list_display = [
        'name',
        'profile',
    ]
    readonly_fields = (
        'created_at',
        'updated_at'
    )
    ordering = ('name',)


admin.site.register(DefaultTable, DefaultTableAdmin)
admin.site.register(UserTable, UserTableAdmin)
