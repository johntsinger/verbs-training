from typing import Any
from django.test.runner import DiscoverRunner
from django.conf import settings


class MyTestRunner(DiscoverRunner):
    def setup_test_environment(self, **kwargs: Any) -> None:
        """Set IS_TEST settings to True during tests."""
        super(MyTestRunner, self).setup_test_environment(**kwargs)
        settings.IS_TEST = True

    def teardown_test_environment(self, **kwargs: Any) -> None:
        """Set IS_TEST settings to False after testing is complete."""
        settings.IS_TEST = False
        super().teardown_test_environment(**kwargs)
