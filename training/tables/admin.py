from typing import Any

from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import (
    FilteredSelectMultiple,
    RelatedFieldWidgetWrapper,
)
from django.db.models import Q
from django.db.models.fields.related import ForeignKey
from django.db.models.query import QuerySet
from django.http import HttpRequest

from training.common.admin.mixins import GetReadOnlyFieldsMixin
from training.profiles.models import Profile
from training.tables.models import DefaultTable, Table, UserTable
from training.verbs.models import Verb


class TableAdminFormMixin:
    """
    Mixin to set initial verbs in tables change form.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["verbs"].initial = self.instance.verbs.all()


class TableAdminForm(TableAdminFormMixin, forms.ModelForm):
    # owner = forms.ModelChoiceField(
    #     queryset=Profile.objects.select_related('user'),
    #     required=False
    # )
    verbs = forms.ModelMultipleChoiceField(
        queryset=Verb.objects.all(),
        required=False,
        # Using RelatedFieldWidgetWrapper prevent label after fields
        widget=RelatedFieldWidgetWrapper(
            FilteredSelectMultiple(
                verbose_name="Verbs",
                is_stacked=False,
            ),
            rel=Table._meta.get_field("verbs").remote_field,
            admin_site=admin.site,
            can_add_related=True,
        ),
    )

    class Meta:
        model = Table
        fields = [
            "type",
            "name",
            "owner",
            "verbs",
            "is_available",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["owner"].required = False

    def clean(self):
        table_type = self.cleaned_data.get("type")
        owner = self.cleaned_data.get("owner")
        if table_type == self.Meta.model.USER_TABLE and not owner:
            raise forms.ValidationError({"owner": "This field is required."})
        if table_type == self.Meta.model.DEFAULT_TABLE and owner:
            raise forms.ValidationError(
                {
                    "owner": (
                        "Default table must not have an owner. "
                        "Leave this field blank."
                    )
                }
            )
        return super().clean()


class DefaultTableAdminForm(TableAdminFormMixin, forms.ModelForm):
    verbs = forms.ModelMultipleChoiceField(
        queryset=Verb.objects.all(),
        required=False,
        # Using RelatedFieldWidgetWrapper prevent label after fields
        widget=RelatedFieldWidgetWrapper(
            FilteredSelectMultiple(
                verbose_name="Verbs",
                is_stacked=False,
            ),
            rel=DefaultTable._meta.get_field("verbs").remote_field,
            admin_site=admin.site,
            can_add_related=True,
        ),
    )

    class Meta:
        model = DefaultTable
        fields = [
            "name",
            "verbs",
            "is_available",
        ]


class UserTableAdminForm(TableAdminFormMixin, forms.ModelForm):
    verbs = forms.ModelMultipleChoiceField(
        queryset=Verb.objects.all(),
        required=False,
        # Using RelatedFieldWidgetWrapper prevent label after fields
        widget=RelatedFieldWidgetWrapper(
            FilteredSelectMultiple(
                verbose_name="Verbs",
                is_stacked=False,
            ),
            rel=UserTable._meta.get_field("verbs").remote_field,
            admin_site=admin.site,
            can_add_related=True,
        ),
    )

    class Meta:
        model = UserTable
        fields = [
            "name",
            "owner",
            "verbs",
            "is_available",
        ]


@admin.register(DefaultTable)
class DefaultTableAdmin(GetReadOnlyFieldsMixin, admin.ModelAdmin):
    form = DefaultTableAdminForm
    list_display = ["name"]
    readonly_fields = [
        "slug_name",
        "created_at",
        "updated_at",
    ]
    search_fields = ["name"]
    search_help_text = "Search default tables by name."
    ordering = ("name",)
    list_per_page = 50


@admin.register(UserTable)
class UserTableAdmin(GetReadOnlyFieldsMixin, admin.ModelAdmin):
    form = UserTableAdminForm
    list_display = [
        "name",
        "owner",
    ]
    readonly_fields = [
        "slug_name",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "name",
        "owner__user__username",
    ]
    search_help_text = "Search user tables by name and owner."
    autocomplete_fields = ["owner"]
    ordering = ("name",)
    list_per_page = 50

    def get_queryset(self, request: HttpRequest) -> QuerySet[UserTable]:
        queryset = super().get_queryset(request)
        return queryset.select_related("owner__user")

    def formfield_for_foreignkey(
        self, db_field: ForeignKey[Any], request: HttpRequest | None, **kwargs: Any
    ) -> forms.ModelChoiceField | None:
        # Select user to display foreignkey profile choices
        # to avoid duplicated query because profile's str method
        # access to user.username
        if db_field.name == "owner":
            kwargs["queryset"] = Profile.objects.select_related("user")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    form = TableAdminForm
    list_display = [
        "name",
        "owner",
        "type",
    ]
    readonly_fields = [
        "slug_name",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "name",
        "owner__user__username",
    ]
    search_help_text = "Search user tables by name and owner."
    autocomplete_fields = ["owner"]
    ordering = ("name",)
    list_per_page = 50

    class Media:
        js = ("js/disableOwner.js",)

    def get_search_results(
        self, request: HttpRequest, queryset: QuerySet[Any], search_term: str
    ) -> tuple[QuerySet[Any], bool]:
        queryset, may_have_duplicates = super().get_search_results(
            request,
            queryset,
            search_term,
        )
        profile_id = request.GET.get("id_profile", None)

        # Returns an empty list to avoid obtaining a result
        # if the profile has not been selected
        if not profile_id and request.get_full_path() != "/admin/tables/table/":
            return Table.objects.none(), may_have_duplicates

        # Return all tables to display on Table admin panel
        if request.get_full_path() == "/admin/tables/table/":
            return (
                Table.objects.all().select_related("owner__user").order_by("type"),
                may_have_duplicates,
            )

        queryset = (
            queryset.filter(Q(owner=profile_id) | Q(type=Table.DEFAULT_TABLE))
            .filter(name__icontains=search_term)
            .order_by("type")
        )
        return queryset, may_have_duplicates

    def get_queryset(self, request: HttpRequest) -> QuerySet[UserTable]:
        queryset = super().get_queryset(request)
        return queryset.select_related("owner__user")

    def formfield_for_foreignkey(
        self, db_field: ForeignKey[Any], request: HttpRequest | None, **kwargs: Any
    ) -> forms.ModelChoiceField | None:
        # Select user to display foreignkey profile choices
        # to avoid duplicated query because profile's str method
        # access to user.username
        if db_field.name == "owner":
            kwargs["queryset"] = Profile.objects.select_related("user")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # def has_module_permission(self, request):
    #     # Avoids displaying Table in the admin panel,
    #     # displays the DefaltTable and UserTable proxy models instead
    #     return False
