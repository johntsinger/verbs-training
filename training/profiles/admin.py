from django.contrib import admin
from profiles.models import Profile, UserVerb, UserTable


admin.site.register(Profile)
admin.site.register(UserVerb)
admin.site.register(UserTable)
