from django.contrib import admin
from verbs.models import Verb


class VerbAdmin(admin.ModelAdmin):
    list_display = [
        'infinitive',
        'simple_past',
        'past_participle',
        'translation'
    ]
    ordering = ('infinitive',)


admin.site.register(Verb, VerbAdmin)
