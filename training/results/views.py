from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import DeleteView

from training.common.views.mixins import PreviousPageURLMixin, TitleMixin
from training.results.models import Result
from training.tables.models import DefaultTable, UserTable


class BaseResetView(
    TitleMixin,
    PreviousPageURLMixin,
    DeleteView,
):
    """Base view for deleting Result."""

    pk_url_kwarg = "pk"
    query_pk_and_slug = True
    slug_field = "slug_name"
    slug_url_kwarg = "slug_name"
    template_name = "results/reset.html"

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on fetched Result objects and redirect
        to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        results = self.get_results()
        results.delete()
        return HttpResponseRedirect(success_url)

    def form_valid(self, form):
        """
        Delete results on form validation and redirect to success URL.
        """
        success_url = self.get_success_url()
        results = self.get_results()
        results.delete()
        return HttpResponseRedirect(success_url)

    def get_previous_page_url(self):
        """
        Should return the DetailView url, which is the same url as the
        get_success_url method of DefaultTableResetView and
        UserTableResetView views returns.
        """
        return self.get_success_url()

    def get_results(self):
        """
        Return a queryset of Result objects to delete.
        Must be implemented in subclasses.
        """
        raise NotImplementedError("Subclasses must implement get_results()")


class AllTablesResetView(BaseResetView):
    """
    View for deleting all Result objects related to the logged-in user
    profile.
    """

    model = Result
    success_url = reverse_lazy("verbs:list")
    title = _("Reset all")

    def get_object(self):
        # We don't want to retreive a single object as we are deleting
        # the Result queryset.
        return None

    def get_results(self):
        return self.model.objects.filter(owner=self.request.user.profile)

    def get_success_url(self):
        return self.success_url


class DefaultTableResetView(BaseResetView):
    """
    View for deleting all Result objects belonging to a DefaultTable
    and related to the logged-in user's profile.
    """

    model = DefaultTable

    def get_results(self):
        return self.object.results.filter(owner=self.request.user.profile)

    def get_success_url(self):
        return reverse(
            "tables:default:detail",
            kwargs={"pk": self.object.id, self.slug_field: self.object.slug_name},
        )

    def get_title(self):
        return gettext(
            "Reset table - %(name)s" % {"name": self.object.name.capitalize()}
        )


class UserTableResetView(BaseResetView):
    """
    View for deleting all Result objects belonging to a UserTable
    and related to the logged-in user's profile.
    """

    model = UserTable

    def get_results(self):
        return self.object.results.all()

    def get_success_url(self):
        return reverse(
            "tables:user:detail",
            kwargs={"pk": self.object.id, "slug_name": self.object.slug_name},
        )

    def get_title(self):
        return gettext(
            "Reset table - %(name)s" % {"name": self.object.name.capitalize()}
        )
