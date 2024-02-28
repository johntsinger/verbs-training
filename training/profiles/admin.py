from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms
from profiles.models import Profile, UserVerb
from tables.models import UserTable


class ProfileAdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'user',
            'tables'
        ]

    tables = forms.ModelMultipleChoiceField(
        queryset=UserTable.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Tables',
            is_stacked=False
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['tables'].initial = self.instance.user_tables.all()

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()

        if profile.pk:
            profile.tables.set(
                self.cleaned_data['tables']
            )
            self.save_m2m()

        return profile


class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm


admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserVerb)
