from django.test import TestCase
from django.urls import reverse_lazy

from verbs.models import Verb
from verbs.tests.fixtures import TestDataFixture


class TestVerbsViews(TestDataFixture, TestCase):
    url = reverse_lazy('verbs-list')

    def test_get_verbs_list_page(self):
        """Test status code, template and queryset."""
        template_expected = 'verbs/verbs_list.html'
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            200
        )
        self.assertTemplateUsed(response, template_expected)
        self.assertQuerysetEqual(
            response.context.get('verb_list', None),
            Verb.objects.all(),
            transform=lambda x: x,
            ordered=False
        )
