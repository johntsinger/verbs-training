from typing import Any

from django import forms
from django.contrib import admin
from django.db.models.fields.related import ForeignKey
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html

from training.common.admin.mixins import GetReadOnlyFieldsMixin
from training.profiles.models import Profile
from training.results.models import Result
from training.tables.models import Table


class ResultAdminChangeForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = [
            "owner",
            "verb",
            "is_success",
        ]


class ResultAdminAddForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = [
            "owner",
            "table",
            "verb",
            "is_success",
        ]


@admin.register(Result)
class ResultAdmin(GetReadOnlyFieldsMixin, admin.ModelAdmin):
    change_form = ResultAdminChangeForm
    add_form = ResultAdminAddForm
    list_display = [
        "owner",
        "table",
        "verb",
        "is_success",
    ]
    list_display_links = [
        "owner",
        "table",
        "verb",
    ]
    readonly_fields = [
        "owner",
        "get_table",
        "verb",
        "created_at",
        "updated_at",
    ]
    autocomplete_fields = [
        "owner",
        "table",
        "verb",
    ]
    search_fields = [
        "owner__user__username",
        "table__name",
        "verb__infinitive",
    ]
    search_help_text = "Search results by owner, table name and verb infinitive."
    list_filter = [
        ("is_success", admin.BooleanFieldListFilter),
    ]
    list_per_page = 50

    class Media:
        css = {"all": ("css/custom-admin.css",)}
        js = ("js/resultsSelect2.js",)

    # Create admin url for table change for proxy models UserTable
    # and DefaultTable.
    @admin.display(description="Table")
    def get_table(self, obj):

        change_url = reverse(
            f"admin:{Table._meta.app_label}_" f"{obj.table.type}_change",
            args=(obj.table.id,),
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
            "owner__user",
            "table__owner__user",
        )

    def formfield_for_foreignkey(
        self,
        db_field: ForeignKey[Any],
        request: HttpRequest | None,
        **kwargs: Any,
    ) -> forms.ModelChoiceField | None:
        # Select related user to display owner and table choices
        # to avoid duplicated queries because profile and table str method
        # access to user.username
        if db_field.name == "owner":
            kwargs["queryset"] = Profile.objects.select_related("user")
        if db_field.name == "table":
            kwargs["queryset"] = Table.objects.select_related("owner__user")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
