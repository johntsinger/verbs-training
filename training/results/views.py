from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import DeleteView

from common.views.mixins import TitleMixin, PreviousPageURLMixin
from results.models import Result
from tables.models import UserTable, DefaultTable


class BaseResetView(
    TitleMixin,
    PreviousPageURLMixin,
    DeleteView,
):
    """
    Base reset view.
    Delete Result objects.
    """
    pk_url_kwarg = 'pk'
    query_pk_and_slug = True
    slug_field = 'slug_name'
    slug_url_kwarg = 'slug_name'
    template_name = 'results/reset.html'

    def form_valid(self, form):
        verbs = self.get_verbs()
        verbs.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_verbs(self):
        if self.object is not None:
            return self.object.results.all()
        return self.get_queryset()

    def get_previous_page_url(self):
        """
        Should return the DetailView url, which is the same url as the
        get_success_url method of DefaultTableResetView and
        UserTableResetView views returns.
        """
        return self.get_success_url()


class AllTablesResetView(BaseResetView):
    model = Result
    success_url = reverse_lazy('verbs:list')
    title = _('Reset all')

    def get_object(self):
        return None

    def get_queryset(self):
        return self.model.objects.filter(
            profile=self.request.user.profile
        )

    def get_success_url(self):
        return self.success_url


class DefaultTableResetView(BaseResetView):
    model = DefaultTable

    def get_success_url(self):
        return reverse(
            'tables:default:detail',
            kwargs={
                'pk': self.object.id,
                'slug_name': self.object.slug_name
            }
        )

    def get_title(self):
        return gettext(
            'Reset table - %(name)s' % {'name': self.object.name.capitalize()}
        )


class UserTableResetView(BaseResetView):
    model = UserTable

    def get_queryset(self):
        return self.model.objects.filter(
            owner=self.request.user.profile
        )

    def get_success_url(self):
        return reverse(
            'tables:user:detail',
            kwargs={
                'pk': self.object.id,
                'slug_name': self.object.slug_name
            }
        )

    def get_title(self):
        return gettext(
            'Reset table - %(name)s' % {'name': self.object.name.capitalize()}
        )
