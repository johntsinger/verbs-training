from django.contrib.auth.decorators import login_not_required
from django.db.models import Subquery, OuterRef
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic.list import ListView

from common.views.mixins import TitleMixin
from verbs.models import Verb
from results.models import Result


@method_decorator(login_not_required, name="dispatch")
class VerbListView(
    TitleMixin,
    ListView
):
    template_name = 'verbs/verb_list.html'
    title = _('Verbs')

    def get_queryset(self):
        """
        Get all verbs and add is_success field based on the Result
        subquery is_success field
        """
        if self.request.user.is_authenticated:
            return Verb.objects.annotate(
                is_success=Subquery(
                    Result.objects.filter(
                        verb=OuterRef('id'),
                        profile=self.request.user.profile,
                    ).order_by(
                        '-updated_at'
                    ).values('is_success')[:1]
                )
            ).prefetch_related(
                'info',
                'examples',
            )

        return Verb.objects.prefetch_related('info', 'examples')
