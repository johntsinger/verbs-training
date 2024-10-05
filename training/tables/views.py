from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Prefetch, Subquery, OuterRef
from django.utils.translation import gettext_lazy as _
from django.views.generic.list import ListView

from common.views.mixins import TitleMixin
from tables.models import Table, DefaultTable, UserTable
from results.models import Result
from verbs.models import Verb


class TableListView(
    TitleMixin,
    LoginRequiredMixin,
    ListView
):
    model = Table
    template_name = 'tables/tables_list.html'
    title = _('Tables')

    def get_queryset(self):
        # Subquery to get is_success for each Verb
        result_subquery = Result.objects.filter(
            profile=self.request.user.profile,
            table=OuterRef('tables'),
            verb=OuterRef('pk')
        ).values('is_success')[:1]

        # Prefetch related verbs with the annotated is_success
        verbs_prefetch = Prefetch(
            'verbs',
            queryset=Verb.objects.annotate(
                is_success=Subquery(result_subquery)
            ).distinct().order_by('infinitive'),
        )

        queryset = Table.objects.filter(
            Q(owner=self.request.user.profile)
            | Q(type='defaulttable')
        ).prefetch_related(verbs_prefetch)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # # Subquery to get is_success for each Verb
        # result_subquery = Result.objects.filter(
        #     profile=self.request.user.profile,
        #     table=OuterRef('tables'),
        #     verb=OuterRef('pk')
        # ).values('is_success')[:1]

        # # Prefetch related verbs with the annotated is_success
        # verbs_prefetch = Prefetch(
        #     'verbs',
        #     queryset=Verb.objects.annotate(
        #         is_success=Subquery(result_subquery)
        #     ).distinct().order_by('infinitive'),
        # )

        # # Query all default tables with the annotated verbs
        # default_tables = DefaultTable.objects.prefetch_related(verbs_prefetch)

        # # Query all user tables with the annotated verbs
        # user_tables = UserTable.objects.filter(
        #     owner=self.request.user.profile
        # ).select_related('owner').prefetch_related(verbs_prefetch)

        # context['default_tables'] = default_tables
        # context['user_tables'] = user_tables

        queryset = self.get_queryset()

        context['default_tables'] = queryset.filter(
            type='defaulttable'
        )
        context['user_tables'] = queryset.filter(
            type='usertable'
        )

        return context
