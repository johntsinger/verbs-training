from typing import Any
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from django.db.models.fields.related import ForeignKey
from django.db.models.query import QuerySet
from django.http import HttpRequest
from results.models import Result
from profiles.models import Profile
from itertools import chain
from tables.models import DefaultTable, UserTable


class ResultAdminForm(forms.ModelForm):

    table = forms.ChoiceField()

    class Meta:
        model = Result
        fields = [
            "verb",
            "profile",
            "default_table",
            "user_table",
            "table",
            "is_success"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        qs = list(chain(DefaultTable.objects.all(), UserTable.objects.all()))
        choices = [
            (None, "---------")
        ]
        choices.extend(
            (
                obj.id,
                f"{obj.name} ({obj.profile})"
                if obj.__class__.__name__ == "UserTable"
                else f"{obj.name}"
            ) for obj in qs
        )
        self.fields["table"].choices = choices
        if not self.instance._state.adding:
            self.fields["table"].initial = self.instance.table.id
        self.fields["default_table"].widget = forms.HiddenInput()
        self.fields["user_table"].widget = forms.HiddenInput()

    def clean(self) -> dict[str, Any]:
        try:
            table = DefaultTable.objects.get(id=self.cleaned_data['table'])
            self.cleaned_data['default_table'] = table
            self.cleaned_data['user_table'] = None
        except ObjectDoesNotExist:
            table = UserTable.objects.get(id=self.cleaned_data['table'])
            self.cleaned_data['user_table'] = table
            self.cleaned_data['default_table'] = None

        print(self.cleaned_data)

        return super().clean()


class ResultAdmin(
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
        "created_at",
        "updated_at"
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

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing
            return self.readonly_fields
        return ()


admin.site.register(Result, ResultAdmin)
