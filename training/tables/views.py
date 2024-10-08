from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Prefetch, Subquery, OuterRef
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from common.views.mixins import TitleMixin, PreviousPageURLMixin
from tables.models import Table
from results.models import Result
from verbs.models import Verb


class TableListView(
    TitleMixin,
    LoginRequiredMixin,
    ListView
):
    model = Table
    template_name = 'tables/table_list.html'
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
        queryset = self.get_queryset()
        context['default_tables'] = queryset.filter(
            type='defaulttable'
        )
        context['user_tables'] = queryset.filter(
            type='usertable'
        )

        return context


class TableDetailView(
    TitleMixin,
    PreviousPageURLMixin,
    LoginRequiredMixin,
    DetailView
):
    title = None
    previous_page_url = reverse_lazy('tables:list')

    def get_queryset(self):
        table_id = self.kwargs.get(self.pk_url_kwarg)
        # Subquery to get is_success for each Verb
        result_subquery = Result.objects.filter(
            profile=self.request.user.profile,
            table_id=table_id,
            verb=OuterRef('pk')
        ).values('is_success')[:1]

        # Prefetch related verbs with the annotated is_success
        verbs_prefetch = Prefetch(
            'verbs',
            queryset=Verb.objects.annotate(
                is_success=Subquery(result_subquery)
            ).prefetch_related('info', 'examples').order_by('infinitive'),
        )
        queryset = Table.objects.filter(
            Q(owner=self.request.user.profile)
            | Q(type='defaulttable')
        )

        return queryset.prefetch_related(verbs_prefetch)

    def get_title(self):
        return self.object.name
