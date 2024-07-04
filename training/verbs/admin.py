from typing import Any

from django import forms
from django.http import HttpRequest
from django.contrib import admin
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet

from verbs.models import Verb, Similarity, Info, Example
from tables.models import Table
from results.models import Result

from common.admin.mixins import GetReadOnlyFieldsMixin


class InfoInline(admin.StackedInline):
    model = Info
    extra = 0
    formfield_overrides = {
        models.CharField: {
            "widget": forms.TextInput(attrs={"size": "150"})
        },
    }

    def get_queryset(self, request: HttpRequest) -> models.QuerySet[Info]:
        queryset = super().get_queryset(request)
        return queryset.select_related("verb")


class ExampleInline(admin.StackedInline):
    model = Example
    extra = 0
    formfield_overrides = {
        models.CharField: {
            "widget": forms.TextInput(attrs={"size": "150"})
        },
    }

    def get_queryset(self, request: HttpRequest) -> models.QuerySet[Example]:
        queryset = super().get_queryset(request)
        return queryset.select_related("verb")


@admin.register(Verb)
class VerbAdmin(admin.ModelAdmin):
    list_display = [
        "infinitive",
        "simple_past",
        "past_participle",
        "translation",
        "similarity",
    ]
    inlines = [
        InfoInline,
        ExampleInline
    ]
    search_fields = [
        "infinitive",
        "simple_past",
        "past_participle",
        "translation"
    ]
    search_help_text = (
        "Search verbs by infinitive, simple past, "
        "past participle or translation"
    )
    autocomplete_fields = ["similarity"]
    ordering = ("infinitive",)
    list_per_page = 50

    def get_queryset(self, request: HttpRequest) -> models.QuerySet[Verb]:
        queryset = super().get_queryset(request)
        return queryset.select_related(
            "similarity"
        )

    def get_search_results(
        self,
        request: HttpRequest,
        queryset: models.QuerySet[Any],
        search_term: str
    ) -> tuple[QuerySet[Any], bool]:
        queryset, may_have_duplicates = super().get_search_results(
            request,
            queryset,
            search_term,
        )
        profile_id = request.GET.get("id_profile", None)
        table_id = request.GET.get("id_table", None)

        # returns original queryset for admin list view search bar
        if (
            "autocomplete" not in request.path
            or request.GET.get('app_label', None) != "results"
        ):
            return queryset, may_have_duplicates

        # returns an empty list to avoid obtaining a result
        # if the table has not been selected
        if not table_id:
            return [], may_have_duplicates

        # verb ids that already have a result for this profile and this table
        excluded_verbs = Result.objects.filter(
            profile=profile_id,
            table=table_id
        ).values_list("verb_id", flat=True)

        queryset = Table.objects.get(
            id=table_id
        ).verbs.exclude(
            id__in=excluded_verbs
        ).filter(
            Q(infinitive__icontains=search_term)
            | Q(simple_past__icontains=search_term)
            | Q(past_participle__icontains=search_term)
            | Q(translation__icontains=search_term)
        ).order_by(
            "infinitive"
        )
        return queryset, may_have_duplicates


@admin.register(Info)
class InfoAdmin(
    GetReadOnlyFieldsMixin,
    admin.ModelAdmin
):
    list_display = [
        "get_verb",
        "content"
    ]
    readonly_fields = ['verb']
    search_fields = ["verb__infinitive"]
    search_help_text = (
        "Search info by verb infinitive."
    )
    autocomplete_fields = ['verb']
    ordering = ("verb__infinitive",)
    list_per_page = 50

    class Media:
        css = {
            "all": ("css/custom-admin.css",)
        }

    @admin.display(
        ordering="verb__infinitive",
        description="Verb"
    )
    def get_verb(self, obj: Info) -> str:
        return obj.verb.infinitive

    def get_queryset(self, request: HttpRequest) -> models.QuerySet[Info]:
        queryset = super().get_queryset(request)
        return queryset.select_related("verb")


@admin.register(Example)
class ExampleAdmin(
    GetReadOnlyFieldsMixin,
    admin.ModelAdmin
):
    list_display = [
        "get_verb",
        "english",
        "translation"
    ]
    readonly_fields = ['verb']
    search_fields = ["verb__infinitive"]
    search_help_text = (
        "Search examples by verb infinitive."
    )
    autocomplete_fields = ['verb']
    ordering = ("verb__infinitive",)
    list_per_page = 50

    class Media:
        css = {
            "all": ("css/custom-admin.css",)
        }

    @admin.display(
        ordering="verb__infinitive",
        description="Verb"
    )
    def get_verb(self, obj: Example) -> str:
        return obj.verb.infinitive

    def get_queryset(self, request: HttpRequest) -> models.QuerySet[Example]:
        queryset = super().get_queryset(request)
        return queryset.select_related("verb")


@admin.register(Similarity)
class SimilarityAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    search_help_text = (
        "Search similarities by name."
    )
    list_per_page = 50
