from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from training.results.models import Result
from training.tables.models import DefaultTable
from training.verbs.models import Example, Info, Similarity, Verb


User = get_user_model()


class VerbsViewsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user", email="user@email.com", password="password"
        )
        cls.similarity = Similarity.objects.create(name="similarity name")
        cls.verb = Verb.objects.create(
            infinitive="begin",
            simple_past="began",
            past_participle="begun",
            translation="commencer",
            similarity=cls.similarity,
        )
        cls.info = Info.objects.create(content="info content", verb=cls.verb)
        cls.example = Example.objects.create(
            english="example english", translation="example translation", verb=cls.verb
        )
        cls.default_table = DefaultTable.objects.create(name="default table name")
        cls.default_table.verbs.add(cls.verb)
        cls.result = Result.objects.create(
            verb=cls.verb,
            owner=cls.user.profile,
            table=cls.default_table,
            is_success=True,
        )


class TestVerbsViews(VerbsViewsTestCase):
    url = reverse_lazy("verbs:list")

    def test_get_anonymous_user(self):
        template_expected = "verbs/verb_list.html"
        response = self.client.get(self.url)
        queryset = response.context.get("verb_list")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_expected)
        self.assertQuerySetEqual(queryset, Verb.objects.all())
        self.assertFalse(hasattr(queryset.first(), "is_success"))

    def test_get_authenticated_user(self):
        template_expected = "verbs/verb_list.html"
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        queryset = response.context.get("verb_list")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_expected)
        self.assertQuerySetEqual(queryset, Verb.objects.all())
        self.assertTrue(hasattr(queryset.first(), "is_success"))
