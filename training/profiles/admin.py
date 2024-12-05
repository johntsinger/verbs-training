from django.contrib import admin
from django.db import models
from django.http import HttpRequest

from training.common.admin.mixins import GetReadOnlyFieldsMixin
from training.common.admin.utils import reverse_foreignkey_change_links
from training.profiles.models import Profile
from training.tables.models import DefaultTable, UserTable


@admin.register(Profile)
class ProfileAdmin(GetReadOnlyFieldsMixin, admin.ModelAdmin):
    list_display = ["user"]
    readonly_fields = (
        "user",
        "default_tables",
        "user_tables",
        "created_at",
        "updated_at",
    )
    default_tables = reverse_foreignkey_change_links(
        DefaultTable,
        lambda obj: DefaultTable.objects.filter(type=DefaultTable.DEFAULT_TABLE),
        description="Default tables",
    )
    user_tables = reverse_foreignkey_change_links(
        UserTable,
        lambda obj: UserTable.objects.filter(
            type=UserTable.USER_TABLE, owner=obj
        ).select_related("owner__user"),
        description="User tables",
    )
    autocomplete_fields = ["user"]
    search_fields = ["user__username"]
    search_help_text = "Search profiles by user."
    ordering = ["user__username"]
    list_per_page = 50

    class Media:
        css = {"all": ("css/custom-admin.css",)}

    def get_queryset(self, request: HttpRequest) -> models.QuerySet[Profile]:
        queryset = super().get_queryset(request)
        return queryset.select_related(
            "user",
        ).order_by("user__username")
