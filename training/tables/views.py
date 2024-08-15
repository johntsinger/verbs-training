from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django.views.generic.list import ListView

from common.views.mixins import TitleMixin
from tables.models import Table


class TableListView(
    TitleMixin,
    LoginRequiredMixin,
    ListView
):
    model = Table
    template_name = 'tables/tables_list.html'
    title = _('All tables')

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        return queryset.select_related(
            'owner'
        ).prefetch_related(
            'verbs'
        ).filter(
            Q(owner=self.request.user.profile)
            | Q(type='defaulttable')
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['default_tables'] = self.object_list.filter(
            type='defaulttable'
        )
        context['user_tables'] = self.object_list.filter(
            type='usertable'
        )
        return context
