from django.core.exceptions import ImproperlyConfigured


class PreviousPageURLMixin:
    """
    Provides a previous page URL attribute and pass it to
    the context.
    """

    previous_page_url = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_page_url"] = self.get_previous_page_url()
        return context

    def get_previous_page_url(self):
        """
        Retruns the URL to redirect after clicking
        on 'return' button.
        """
        if not self.previous_page_url:
            raise ImproperlyConfigured(
                "%(cls)s is missing a Previous page url. Define "
                "%(cls)s.previous_page_url, or override "
                "%(cls)s.get_previous_page_url()." % {"cls": self.__class__.__name__}
            )
        return self.previous_page_url


class TitleMixin:
    """Provide a title attribute and pass it to the context."""

    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_title()
        return context

    def get_title(self):
        if not self.title:
            raise ImproperlyConfigured(
                "%(cls)s is missing a Title. Define "
                "%(cls)s.title, or override "
                "%(cls)s.get_title()." % {"cls": self.__class__.__name__}
            )
        return self.title
