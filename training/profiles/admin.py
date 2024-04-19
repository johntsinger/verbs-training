from django.contrib import admin
from common.admin.mixins import GetReadOnlyFieldsMixin
from common.admin.utils import reverse_foreignkey_change_links
from profiles.models import Profile
from tables.models import DefaultTable, UserTable


class ProfileAdmin(
    GetReadOnlyFieldsMixin,
    admin.ModelAdmin
):
    readonly_fields = (
        'created_at',
        'updated_at',
        'default_tables',
        'user_tables'
    )
    default_tables = reverse_foreignkey_change_links(
        DefaultTable,
        lambda obj: DefaultTable.objects.filter(is_available=True),
        description='Default tables'
    )
    user_tables = reverse_foreignkey_change_links(
        UserTable,
        lambda obj: UserTable.objects.filter(profile=obj),
        description='User tables'
    )


admin.site.register(Profile, ProfileAdmin)
