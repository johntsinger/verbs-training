import random
import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Prefetch, Subquery, OuterRef
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from common.views.mixins import TitleMixin, PreviousPageURLMixin
from results.models import Result
from tables.models import Table
from tables.forms import VerbFormSet
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
    pk_url_kwarg = 'pk'
    slug_url_kwarg = 'slug_name'
    slug_field = 'slug_name'
    query_pk_and_slug = True

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


class TrainingFormView(
    TitleMixin,
    PreviousPageURLMixin,
    LoginRequiredMixin,
    SingleObjectMixin,
    FormView
):
    template_name = 'tables/training.html'
    form_class = VerbFormSet
    pk_url_kwarg = 'pk'
    slug_url_kwarg = 'slug_name'
    slug_field = 'slug_name'
    query_pk_and_slug = True

    def get_success_url(self):
        return reverse(
            'tables:results',
            kwargs={
                'pk': self.object.id,
                'slug_name': self.object.slug_name
            }
        )

    def get_queryset(self):
        return Table.objects.filter(
            Q(owner=self.request.user.profile)
            | Q(type='defaulttable')
        ).prefetch_related('verbs')

    def get_verbs_sample(self):
        verbs = list(self.object.verbs.all())
        return random.sample(verbs, 10)

    def get_verbs(self):
        if (
            self.request.session.get('verbs', None) is None
            or self.request.method == 'GET'
        ):
            verbs_sample = self.get_verbs_sample()
            verbs_id = [str(verb.id) for verb in verbs_sample]
            self.request.session['verbs_id'] = verbs_id
        return self.object.verbs.filter(
            id__in=self.request.session['verbs_id']
        )

    def get_initial(self):
        return self.verbs.values('translation')

    def set_result(self, verb_id, is_success):
        result, _ = Result.objects.get_or_create(
            profile=self.request.user.profile,
            table_id=self.object.id,
            verb_id=verb_id
        )
        result.is_success = is_success
        result.save()

    def get_data(self, cleaned_data, verb):
        data = cleaned_data | {
            'correct_infinitive': verb.infinitive,
            'correct_simple_past': verb.simple_past,
            'correct_past_participle': verb.past_participle,
            'translation': verb.translation,
            'infinitive_is_success': (
                cleaned_data.get('infinitive')
                in re.split(', |/', verb.infinitive)
            ),
            'simple_past_is_success': (
                cleaned_data.get('simple_past')
                in re.split(', |/', verb.simple_past)
            ),
            'past_participle_is_success': (
                cleaned_data.get('past_participle')
                in re.split(', |/', verb.past_participle)
            ),
        }
        data['is_success'] = all(
            [
                data['infinitive_is_success'],
                data['simple_past_is_success'],
                data['past_participle_is_success']
            ]
        )
        return data

    def form_valid(self, form):
        data = []
        for cleaned_data, verb in zip(
            form.cleaned_data,
            self.verbs
        ):
            verb_data = self.get_data(cleaned_data, verb)
            self.set_result(
                verb_id=verb.id,
                is_success=verb_data['is_success']
            )
            data.append(verb_data)
        self.request.session['results'] = data
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.verbs = self.get_verbs()
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.verbs = self.get_verbs()
        return super().get(request, *args, **kwargs)

    def get_previous_page_url(self):
        return reverse(
            'tables:detail',
            kwargs={
                'pk': self.object.id,
                'slug_name': self.object.slug_name
            }
        )

    def get_title(self):
        return f'{self.object.name} - Training'


class ResultView(
    TitleMixin,
    PreviousPageURLMixin,
    LoginRequiredMixin,
    TemplateView
):
    template_name = 'tables/results.html'
    pk_url_kwarg = 'pk'
    slug_url_kwargs = 'slug_name'

    def get_previous_page_url(self):
        return reverse(
            'tables:detail',
            kwargs={
                'pk': self.object.id,
                'slug_name': self.object.slug_name
            }
        )

    def get_object(self):
        return Table.objects.get(
            id=self.kwargs.get(self.pk_url_kwarg),
            slug_name=self.kwargs.get(self.slug_url_kwargs)
        )

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['results'] = self.request.session.get('results')
        return context

    def get_title(self):
        return f'{self.object.name} - Results'
