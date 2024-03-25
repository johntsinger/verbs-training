from django.contrib import admin
from django import forms
from results.models import Result

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


class ResultAdmin(admin.ModelAdmin):
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

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing
            return self.readonly_fields
        return ()


admin.site.register(Result, ResultAdmin)
