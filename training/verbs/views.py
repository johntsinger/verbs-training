from django.db.models import Subquery, OuterRef
from django.views.generic.list import ListView
from verbs.models import Verb
from results.models import Result


class VerbListView(
    ListView
):
    template_name = 'verbs/verbs.html'

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
            ).prefetch_related('info', 'examples')

        return Verb.objects.prefetch_related('info', 'examples')
