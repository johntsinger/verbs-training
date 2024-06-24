from typing import Any

from django import forms
from django.contrib import admin
from django.db.models.fields.related import ForeignKey
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html
from django.urls import reverse

from results.models import Result
from profiles.models import Profile
from tables.models import Table

from common.admin.mixins import GetReadOnlyFieldsMixin
from common.forms.fields import GroupedModelChoiceField


class ResultAdminChangeForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = [
            "verb",
            "profile",
            "is_success"
        ]


class ResultAdminAddForm(forms.ModelForm):
    table = GroupedModelChoiceField(
        queryset=Table.objects.all().select_related(
            'owner__user'
        ).order_by(
            'type',
            '-owner'
        ),
        group_by_field="owner",
        group_label=lambda x: f"User: {x}" if x else 'Default'
    )

    class Meta:
        model = Result
        fields = [
            "verb",
            "profile",
            "table",
            "is_success"
        ]


class ResultAdmin(
    GetReadOnlyFieldsMixin,
    admin.ModelAdmin
):
    change_form = ResultAdminChangeForm
    add_form = ResultAdminAddForm
    list_display = [
        "verb",
        "profile",
        "table",
        "is_success"
    ]
    readonly_fields = (
        "verb",
        "profile",
        "get_table",
        "created_at",
        "updated_at"
    )

    class Media:
        css = {
            "all": ("css/custom-admin.css",)
        }

    # Display table link to change form manually because it
    # doesn't display by it self when using readonly unlike
    # verb and profile
    @admin.display(description="Table")
    def get_table(self, obj):

        change_url = reverse(
            f'admin:{Table._meta.app_label}_'
            f'{obj.table.type}_change',
            args=(obj.table.id, )
        )
        return format_html(
            f'<a href="{change_url}" title="Change">{str(obj.table)}</a>'
        )

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = self.add_form
        else:
            self.form = self.change_form

        return super().get_form(request, obj, **kwargs)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Result]:
        qs = super().get_queryset(request)
        return qs.select_related(
            "verb",
            "profile__user",
            "table__owner__user",
        )

    def formfield_for_foreignkey(
        self,
        db_field: ForeignKey[Any],
        request: HttpRequest | None,
        **kwargs: Any
    ) -> forms.ModelChoiceField | None:
        # Select user to display foreignkey profile and table choices
        # to avoid duplicated query because profile and table str method
        # access to user.username
        if db_field.name == "profile":
            kwargs["queryset"] = Profile.objects.select_related("user")
        if db_field.name == "table":
            kwargs["queryset"] = Table.objects.select_related("owner__user")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Result, ResultAdmin)
