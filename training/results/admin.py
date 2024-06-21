from typing import Any
from django.contrib import admin
from django import forms
from django.db.models.fields.related import ForeignKey
from django.db.models.query import QuerySet
from django.http import HttpRequest
from results.models import Result
from profiles.models import Profile
from tables.models import Table
from common.admin.mixins import GetReadOnlyFieldsMixin


# class ResultAdminForm(forms.ModelForm):

#     table = forms.ChoiceField()

#     class Meta:
#         model = Result
#         fields = [
#             "verb",
#             "profile",
#             "default_table",
#             "user_table",
#             "table",
#             "is_success"
#         ]

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         qs = list(chain(DefaultTable.objects.all(), UserTable.objects.all()))
#         choices = [
#             (None, "---------")
#         ]
#         choices.extend(
#             (
#                 obj.id,
#                 f"{obj.name} ({obj.profile})"
#                 if obj.__class__.__name__ == "UserTable"
#                 else f"{obj.name}"
#             ) for obj in qs
#         )
#         self.fields["table"].choices = choices
#         if not self.instance._state.adding:
#             self.fields["table"].initial = self.instance.table.id
#         self.fields["default_table"].widget = forms.HiddenInput()
#         self.fields["user_table"].widget = forms.HiddenInput()


class ResultAdmin(
    GetReadOnlyFieldsMixin,
    admin.ModelAdmin
):
    # form = ResultAdminForm
    list_display = [
        "verb",
        "profile",
        "table",
        "is_success"
    ]
    readonly_fields = (
        "verb",
        "profile",
        "table",
        "created_at",
        "updated_at"
    )

    class Media:
        css = {
            "all": ("css/custom-admin.css",)
        }

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
