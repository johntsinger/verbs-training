from typing import Any
from django.contrib import admin
from django import forms
from django.db.models.fields.related import ForeignKey
from django.db.models.query import QuerySet
from django.http import HttpRequest
from common.admin.mixins import GetReadOnlyFieldsMixin
from results.models import Result
from profiles.models import Profile

"""
class ResultAdminForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = [
            'profile',
            'table',
            'verb',
            'success'
        ]
"""


class ResultAdmin(
    GetReadOnlyFieldsMixin,
    admin.ModelAdmin
):
    # form = ResultAdminForm
    list_display = [
        'verb',
        'profile',
        'table',
        'is_success'
    ]
    readonly_fields = (
        'created_at',
        'updated_at'
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet[Result]:
        qs = super().get_queryset(request)
        return qs.select_related(
            "verb",
            "profile__user",
            "default_table",
            "user_table",
        )

    def formfield_for_foreignkey(
        self,
        db_field: ForeignKey[Any],
        request: HttpRequest | None,
        **kwargs: Any
    ) -> forms.ModelChoiceField | None:
        # Select user to display foreignkey profile choices
        # to avoid duplicated query because profile's str method
        # access to user.username
        if db_field.name == "profile":
            kwargs["queryset"] = Profile.objects.select_related("user")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Result, ResultAdmin)
