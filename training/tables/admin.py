from typing import Any
from django.contrib import admin
from django.contrib.admin.widgets import (
    FilteredSelectMultiple,
    RelatedFieldWidgetWrapper
)
from django import forms
from django.db.models.fields.related import ForeignKey
from django.db.models.query import QuerySet
from django.http import HttpRequest
from common.admin.mixins import GetReadOnlyFieldsMixin
from tables.models import (
    DefaultTable,
    UserTable
)
from verbs.models import Verb
from profiles.models import Profile


class TableAdminFormMixin:
    """
    Mixin to set initial verbs in tables change form.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["verbs"].initial = self.instance.verbs.all()


class DefaultTableAdminForm(
    TableAdminFormMixin,
    forms.ModelForm
):
    verbs = forms.ModelMultipleChoiceField(
        queryset=Verb.objects.all(),
        required=False,
        # Using RelatedFieldWidgetWrapper prevent label after fields
        widget=RelatedFieldWidgetWrapper(
            FilteredSelectMultiple(
                verbose_name="Verbs",
                is_stacked=False
            ),
            rel=DefaultTable._meta.get_field("verbs").remote_field,
            admin_site=admin.site,
            can_add_related=True
        )
    )

    class Meta:
        model = DefaultTable
        fields = [
            "name",
            "verbs",
            "is_available"
        ]


class UserTableAdminForm(
    TableAdminFormMixin,
    forms.ModelForm
):
    verbs = forms.ModelMultipleChoiceField(
        queryset=Verb.objects.all(),
        required=False,
        # Using RelatedFieldWidgetWrapper prevent label after fields
        widget=RelatedFieldWidgetWrapper(
            FilteredSelectMultiple(
                verbose_name="Verbs",
                is_stacked=False
            ),
            rel=UserTable._meta.get_field("verbs").remote_field,
            admin_site=admin.site,
            can_add_related=True
        )
    )

    class Meta:
        model = UserTable
        fields = [
            "name",
            "owner",
            "verbs",
            "is_available"
        ]


class DefaultTableAdmin(
    GetReadOnlyFieldsMixin,
    admin.ModelAdmin
):
    form = DefaultTableAdminForm
    list_display = [
        "name",
    ]
    readonly_fields = (
        "created_at",
        "updated_at"
    )
    ordering = ("name",)


class UserTableAdmin(
    GetReadOnlyFieldsMixin,
    admin.ModelAdmin
):
    form = UserTableAdminForm
    list_display = [
        "name",
        "owner",
    ]
    readonly_fields = (
        "created_at",
        "updated_at"
    )
    ordering = ("name",)

    def get_queryset(self, request: HttpRequest) -> QuerySet[UserTable]:
        qs = super().get_queryset(request)
        return qs.select_related("owner__user")

    def formfield_for_foreignkey(
        self,
        db_field: ForeignKey[Any],
        request: HttpRequest | None,
        **kwargs: Any
    ) -> forms.ModelChoiceField | None:
        # Select user to display foreignkey profile choices
        # to avoid duplicated query because profile's str method
        # access to user.username
        if db_field.name == "owner":
            kwargs["queryset"] = Profile.objects.select_related("user")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(DefaultTable, DefaultTableAdmin)
admin.site.register(UserTable, UserTableAdmin)
