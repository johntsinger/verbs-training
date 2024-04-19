from django.contrib import admin
from django import forms
from common.admin.mixins import GetReadOnlyFieldsMixin
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


admin.site.register(Result, ResultAdmin)
