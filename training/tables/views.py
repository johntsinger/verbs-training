import re

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q, Prefetch, Subquery, OuterRef
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import (
    FormView, UpdateView, CreateView, DeleteView
)
from django.views.generic.list import ListView

from common.views.mixins import TitleMixin, PreviousPageURLMixin
from results.models import Result
from tables.models import Table, UserTable, DefaultTable
from tables.forms import UserTableForm, DefaultTableForm, VerbFormSet
from verbs.models import Verb


class TableListView(
    TitleMixin,
    ListView
):
    model = Table
    template_name = 'tables/list.html'
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
            | Q(type=Table.DEFAULT_TABLE)
        ).prefetch_related(verbs_prefetch)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context['default_tables'] = queryset.filter(
            type=Table.DEFAULT_TABLE
        )
        context['user_tables'] = queryset.filter(
            type=Table.USER_TABLE
        )
        context['user_tables_count'] = queryset.filter(
            type=Table.USER_TABLE
        ).count()
        return context

        return context


class BaseTableDetailView(
    TitleMixin,
    PreviousPageURLMixin,
    DetailView
):
    """Base view for DefaultTableDetailView and UserTableDetailView."""
    pk_url_kwarg = 'pk'
    previous_page_url = reverse_lazy('tables:list')
    query_pk_and_slug = True
    slug_field = 'slug_name'
    slug_url_kwarg = 'slug_name'
    template_name = 'tables/detail.html'

    def prefetch_verbs(self, table_id):
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

        return verbs_prefetch

    def get_title(self):
        return self.object.name


class DefaultTableDetailView(BaseTableDetailView):
    model = DefaultTable

    def get_queryset(self):
        table_id = self.kwargs.get(self.pk_url_kwarg)
        verbs_prefetch = self.prefetch_verbs(table_id)
        return self.model.objects.prefetch_related(verbs_prefetch)


class UserTableDetailView(BaseTableDetailView):
    model = UserTable

    def get_queryset(self):
        table_id = self.kwargs.get(self.pk_url_kwarg)
        verbs_prefetch = self.prefetch_verbs(table_id)
        return self.model.objects.filter(
            Q(owner=self.request.user.profile)
        ).prefetch_related(verbs_prefetch)


class BaseTableCreateView(
    TitleMixin,
    PreviousPageURLMixin,
    UserPassesTestMixin,
    CreateView
):
    """Base view for DefaultTableCreateView and UserTableCreateView."""
    pk_url_kwarg = 'pk'
    query_pk_and_slug = True
    slug_field = 'slug_name'
    slug_url_kwarg = 'slug_name'
    template_name = 'tables/update.html'
    title = _('Add table')

    def get_previous_page_url(self):
        return reverse('tables:list')


class DefaultTableCreateView(BaseTableCreateView):
    form_class = DefaultTableForm
    model = DefaultTable

    def get_queryset(self):
        return DefaultTable.objects.prefetch_related('verbs')

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse(
            'tables:default:detail',
            kwargs={
                'pk': self.object.id,
                'slug_name': self.object.slug_name
            }
        )


class UserTableCreateView(BaseTableCreateView):
    form_class = UserTableForm
    max_per_user = 10
    model = UserTable

    def get_queryset(self):
        return UserTable.objects.filter(
            owner=self.request.user.profile
        ).prefetch_related('verbs')

    def test_func(self):
        return self.model.objects.filter(
            owner=self.request.user.profile
        ).count() < self.max_per_user

    def handle_no_permission(self):
        messages.error(
            self.request,
            gettext(
                'Maximum number of tables reached '
                '(%(max_per_user)s of %(max_per_user)s).'
                % {'max_per_user': self.max_per_user}
            )
        )
        return redirect('tables:list')

    def get_success_url(self):
        return reverse(
            'tables:user:detail',
            kwargs={
                'pk': self.object.id,
                'slug_name': self.object.slug_name
            }
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['owner'] = self.request.user.profile
        return kwargs


class BaseTableUpdateView(
    TitleMixin,
    PreviousPageURLMixin,
    UpdateView
):
    """Base view for DefaultTableUpdateView and UserTableUpdateView."""
    pk_url_kwarg = 'pk'
    query_pk_and_slug = True
    slug_field = 'slug_name'
    slug_url_kwarg = 'slug_name'
    template_name = 'tables/update.html'

    def get_previous_page_url(self):
        """
        Should return the DetailView url, which is the same url as the
        get_success_url method of DefaultTableResetView and
        UserTableResetView views returns.
        """
        return self.get_success_url()

    def get_title(self):
        return gettext(
            'Edit table - %(name)s' % {'name': self.object.name.capitalize()}
        )


class DefaultTableUpdateView(UserPassesTestMixin, BaseTableUpdateView):
    form_class = DefaultTableForm

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return DefaultTable.objects.prefetch_related('verbs')

    def get_success_url(self):
        return reverse(
            'tables:default:detail',
            kwargs={
                'pk': self.object.id,
                'slug_name': self.object.slug_name
            }
        )


class UserTableUpdateView(BaseTableUpdateView):
    form_class = UserTableForm

    def get_queryset(self):
        return UserTable.objects.filter(
            owner=self.request.user.profile
        ).prefetch_related('verbs')

    def get_success_url(self):
        return reverse(
            'tables:user:detail',
            kwargs={
                'pk': self.object.id,
                'slug_name': self.object.slug_name
            }
        )


class BaseTableDeleteView(
    TitleMixin,
    PreviousPageURLMixin,
    DeleteView
):
    """Base view for DefaultTableResetView and UserTableResetView."""
    pk_url_kwarg = 'pk'
    query_pk_and_slug = True
    slug_field = 'slug_name'
    slug_url_kwarg = 'slug_name'
    success_url = reverse_lazy('tables:list')
    template_name = 'tables/delete.html'

    def get_title(self):
        return gettext(
            'Delete table - %(name)s' % {'name': self.object.name.capitalize()}
        )


class DefaultTableDeleteView(UserPassesTestMixin, BaseTableDeleteView):
    model = DefaultTable

    def test_func(self):
        return self.request.user.is_staff

    def get_previous_page_url(self):
        return reverse(
            'tables:default:detail',
            kwargs={
                'pk': self.object.id,
                'slug_name': self.object.slug_name
            }
        )


class UserTableDeleteView(BaseTableDeleteView):
    def get_queryset(self):
        return UserTable.objects.filter(
            owner=self.request.user.profile
        )

    def get_previous_page_url(self):
        return reverse(
            'tables:user:detail',
            kwargs={
                'pk': self.object.id,
                'slug_name': self.object.slug_name
            }
        )


class BaseTrainingFormView(
    TitleMixin,
    PreviousPageURLMixin,
    SingleObjectMixin,
    FormView
):
    """
    Base view for DefaultTableTrainingFormView and
    UserTableTraingFormView.
    """
    form_class = VerbFormSet
    pk_url_kwarg = 'pk'
    query_pk_and_slug = True
    slug_field = 'slug_name'
    slug_url_kwarg = 'slug_name'
    template_name = 'tables/training.html'
    total_verb_forms = 10

    def get_verbs_sample(self, number):
        """Return a random sample of 'number' verbs from the table"""
        return self.object.verbs.all().order_by('?')[:number]

    def get_verbs(self):
        """
        Get a random sample of verbs belonging to the table and save
        their ids to the session.
        """
        verbs_id = self.request.session.get('verbs_id')
        if not verbs_id or self.request.method == 'GET':
            verbs_sample = self.get_verbs_sample(self.total_verb_forms)
            self.request.session['verbs_id'] = [
                verb.id for verb in verbs_sample
            ]
            return list(verbs_sample)
        # Transform the queryset to list to avoid hitting db
        # multiple time when ittarting over it.
        verbs = list(
            self.object.verbs.filter(
                id__in=verbs_id
            )
        )
        # Sort verbs in same order than verbs_id otherwise cleaned_data
        # does not corresponding.
        verbs.sort(key=lambda verb: verbs_id.index(verb.id))
        return verbs

    def get_initial(self):
        return [{'translation': verb.translation} for verb in self.verbs]

    def get_correct_data(self, verb):
        return {
            'correct_infinitive': verb.infinitive,
            'correct_simple_past': verb.simple_past,
            'correct_past_participle': verb.past_participle,
            'translation': verb.translation,
        }

    def get_verb_success(self, cleaned_data, verb):
        data = {
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
        data['is_success'] = all(data.values())
        return data

    def get_data(self, cleaned_data, verb):
        return (
            cleaned_data
            | self.get_correct_data(verb)
            | self.get_verb_success(cleaned_data, verb)
        )

    def form_valid(self, form):
        verbs_data = []
        results = []
        for cleaned_data, verb in zip(form.cleaned_data, self.verbs):
            data = self.get_data(cleaned_data, verb)
            result = Result(
                profile=self.request.user.profile,
                table_id=self.object.id,
                verb_id=verb.id,
                is_success=data['is_success']
            )
            verbs_data.append(data)
            results.append(result)

        # Save results objects.
        # Update update_fields when a row insertion fails on conflicts.
        # WARNING update_fields not working on Oracle database.
        Result.objects.bulk_create(
            results,
            update_conflicts=True,
            update_fields=['is_success'],
            unique_fields=['profile_id', 'table_id', 'verb_id']
        )
        # self.request.session['results'] = form.cleaned_data
        self.request.session['verbs_data'] = verbs_data
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.verbs = self.get_verbs()
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.verbs = self.get_verbs()
        return super().get(request, *args, **kwargs)

    def get_title(self):
        return gettext(
            '%(name)s - Training' % {'name': self.object.name.capitalize()}
        )


class DefaultTableTrainingFormView(BaseTrainingFormView):
    model = DefaultTable

    def get_queryset(self):
        return self.model.objects.prefetch_related('verbs')

    def get_success_url(self):
        return reverse(
            'tables:default:results',
            kwargs={
                'pk': self.object.id,
                'slug_name': self.object.slug_name
            }
        )

    def get_previous_page_url(self):
        return reverse(
            'tables:default:detail',
            kwargs={
                'pk': self.object.id,
                'slug_name': self.object.slug_name
            }
        )


class UserTableTrainingFormView(BaseTrainingFormView):
    model = UserTable

    def get_queryset(self):
        return self.model.objects.filter(
            owner=self.request.user.profile
        ).prefetch_related('verbs')

    def get_success_url(self):
        return reverse(
            'tables:user:results',
            kwargs={
                'pk': self.object.id,
                'slug_name': self.object.slug_name
            }
        )

    def get_previous_page_url(self):
        return reverse(
            'tables:user:detail',
            kwargs={
                'pk': self.object.id,
                'slug_name': self.object.slug_name
            }
        )


class BaseResultView(
    TitleMixin,
    PreviousPageURLMixin,
    DetailView
):
    """Base view for DefaultTableResultView and UserTableResultView."""
    pk_url_kwarg = 'pk'
    query_pk_and_slug = True
    slug_field = 'slug_name'
    slug_url_kwarg = 'slug_name'
    template_name = 'tables/results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        verbs_data = self.request.session.get('verbs_data')
        if verbs_data is not None:
            context['verbs_data'] = verbs_data
            del self.request.session['verbs_data']
        return context

    def get_title(self):
        return gettext(
            '%(name)s - Results' % {'name': self.object.name.capitalize()}
        )


class DefaultTableResultView(BaseResultView):
    model = DefaultTable

    def get_previous_page_url(self):
        return reverse(
            'tables:default:detail',
            kwargs={
                'pk': self.object.id,
                'slug_name': self.object.slug_name
            }
        )


class UserTableResultView(BaseResultView):
    model = UserTable

    def get_queryset(self):
        return self.model.objects.filter(
            owner=self.request.user.profile
        )

    def get_previous_page_url(self):
        return reverse(
            'tables:user:detail',
            kwargs={
                'pk': self.object.id,
                'slug_name': self.object.slug_name
            }
        )
