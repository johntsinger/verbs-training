from django.core.exceptions import ImproperlyConfigured


class PreviousPageURLMixin:
    """Provides a previous page URL attribute and pass it to the context"""
    previous_page_url = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['previous_page_url'] = self.get_previous_page_url()
        return context

    def get_previous_page_url(self):
        """Retruns the URL to redirect after clicking on 'return' button"""
        if not self.previous_page_url:
            raise ImproperlyConfigured(
                'No URL to return to. Provide a previous_page_url.'
            )
        return self.previous_page_url


class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def get_title(self):
        if not self.title:
            raise ImproperlyConfigured(
                'No title defined. Provide a title.'
            )
        return self.title
