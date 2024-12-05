from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory


class RequestFactoryMixin:
    """Set up request factory for each test case."""

    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()

    def setUp_session(self, request):
        """Set up session if request needs SessionMiddleware."""
        setattr(request, "session", {})

    def setUp_messages(self, request):
        """Set up messages if request needs MessageMiddleware."""

        # message middleware requires session middleware
        self.setUp_session(request)

        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
