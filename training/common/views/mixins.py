from django.core.exceptions import ImproperlyConfigured


class PreviousPageURLMixin:
    """Provide a previous page URL attribute and pass it to the context"""
    previous_page_url = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['previous_page_url'] = self.get_previous_page_url()
        return context

    def get_previous_page_url(self):
        """Retrun the URL to redirect after clicking on 'return' button"""
        if not self.previous_page_url:
            raise ImproperlyConfigured(
                'No URL to return to. Provide a previous_page_url.'
            )
        return self.previous_page_url
