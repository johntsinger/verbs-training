from django.contrib import admin
from django.db import models
from django.http import HttpRequest
from common.admin.mixins import GetReadOnlyFieldsMixin
from common.admin.utils import reverse_foreignkey_change_links
from profiles.models import Profile
from tables.models import DefaultTable, UserTable


class ProfileAdmin(
    GetReadOnlyFieldsMixin,
    admin.ModelAdmin
):
    readonly_fields = (
        'user',
        'default_tables',
        'user_tables',
        'created_at',
        'updated_at',
    )
    default_tables = reverse_foreignkey_change_links(
        DefaultTable,
        lambda obj: DefaultTable.objects.filter(is_default=True),
        description='Default tables'
    )
    user_tables = reverse_foreignkey_change_links(
        UserTable,
        lambda obj: UserTable.objects.filter(
            is_default=False, owner=obj
        ).select_related("owner__user"),
        description='User tables'
    )

    class Media:
        css = {
            "all": ("css/custom-admin.css",)
        }

    def get_queryset(self, request: HttpRequest) -> models.QuerySet[Profile]:
        qs = super().get_queryset(request)
        return qs.select_related(
            'user',
        )


admin.site.register(Profile, ProfileAdmin)
