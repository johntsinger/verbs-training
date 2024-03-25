from django.contrib import admin
from common.admin.utils import reverse_foreignkey_change_links
from profiles.models import Profile
from tables.models import DefaultTable, UserTable


class ProfileAdmin(admin.ModelAdmin):
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

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing
            return self.readonly_fields
        return ()


admin.site.register(Profile, ProfileAdmin)
