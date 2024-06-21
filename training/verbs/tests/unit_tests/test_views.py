from django.test import TestCase  # override_settings
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from verbs.models import Verb, Similarity, Info, Example
from results.models import Result
from tables.models import DefaultTable


User = get_user_model()


class BaseTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="a@a.com",
            password="a",
            username="a"
        )
        cls.similarity = Similarity.objects.create(
            name="similarity name"
        )
        cls.verb = Verb.objects.create(
            infinitive="begin",
            simple_past="began",
            past_participle="begun",
            translation="commencer",
            similarity=cls.similarity
        )
        cls.info = Info.objects.create(
            content="info content",
            verb=cls.verb
        )
        cls.example = Example.objects.create(
            english="example english",
            translation="example translation",
            verb=cls.verb
        )
        cls.default_table = DefaultTable.objects.create(
            name="default table name"
        )
        cls.default_table.verbs.add(cls.verb)
        cls.result = Result.objects.create(
            verb=cls.verb,
            profile=cls.user.profile,
            default_table=cls.default_table,
            is_success=True
        )


class TestVerbsViews(BaseTestCase):
    url = reverse_lazy('verbs')

    def test_list_view(self):
        """Test status code, templates and queryset"""
        templates_expected = {
            "base.html",
            "verbs/verbs.html",
            "base_table.html",
            "includes/navbar.html",
            "includes/messages.html",
            "includes/table.html"
        }
        response = self.client.get(self.url)
        templates_used = {template.name for template in response.templates}

        self.assertEqual(
            response.status_code,
            200
        )
        self.assertEqual(
            templates_used,
            templates_expected
        )
        self.assertQuerysetEqual(
            response.context.get("verb_list", None),
            Verb.objects.all(),
            transform=lambda x: x,
            ordered=False
        )

    def test_list_view_annonymous(self):
        """Test verbs queryset don't have result for anonymous user"""
        response = self.client.get(self.url)
        self.assertRaises(
            AttributeError,
            getattr,
            response.context.get(
                "verb_list", None
            ).get(
                infinitive="begin"
            ),
            "is_success"
        )

    def test_list_view_logged_in(self):
        """Test verbs queryset have results for logged in user"""
        self.client.login(email="a@a.com", password="a")
        response = self.client.get(self.url)
        self.assertTrue(
            response.context.get(
                "verb_list", None
            ).get(
                infinitive="begin"
            ).is_success,
        )
