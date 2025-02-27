from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.urls import reverse, reverse_lazy

from training.results.models import Result
from training.results.views import BaseResetView
from training.tables.models import DefaultTable, UserTable
from training.verbs.models import Verb


User = get_user_model()


class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            username="user1",
            email="user1@email.com",
            password="password",
        )
        cls.user2 = User.objects.create_user(
            username="user2",
            email="user2@email.com",
            password="password",
        )

        cls.verb1 = Verb.objects.create(
            infinitive="begin",
            simple_past="began",
            past_participle="begun",
            translation="commencer",
        )
        cls.verb2 = Verb.objects.create(
            infinitive="become",
            simple_past="became",
            past_participle="become",
            translation="devenir",
        )
        cls.verb3 = Verb.objects.create(
            infinitive="cut",
            simple_past="cut",
            past_participle="cut",
            translation="couper",
        )

        cls.default_table = DefaultTable.objects.create(name="default")
        cls.default_table.verbs.add(*[cls.verb1, cls.verb2, cls.verb3])

        cls.user_table1 = UserTable.objects.create(
            name="table1",
            owner=cls.user1.profile,
        )
        cls.user_table1.verbs.add(*[cls.verb2, cls.verb3])

        cls.user_table2 = UserTable.objects.create(
            name="table2",
            owner=cls.user2.profile,
        )
        cls.user_table2.verbs.add(*[cls.verb1, cls.verb2])

        for verb in cls.default_table.verbs.all():
            Result.objects.create(
                owner=cls.user1.profile,
                table=cls.default_table,
                verb=verb,
                is_success=True,
            )
            Result.objects.create(
                owner=cls.user2.profile,
                table=cls.default_table,
                verb=verb,
                is_success=False,
            )

        for verb in cls.user_table1.verbs.all():
            Result.objects.create(
                owner=cls.user1.profile,
                table=cls.user_table1,
                verb=verb,
                is_success=True,
            )

        for verb in cls.user_table2.verbs.all():
            Result.objects.create(
                owner=cls.user2.profile,
                table=cls.user_table2,
                verb=verb,
                is_success=False,
            )


class TestBaseResetView(BaseTestCase):
    url = reverse_lazy("results:reset-all")
    view_class = BaseResetView

    def setUp(self):
        self.factory = RequestFactory()

    def test_get_results_not_implemented(self):
        request = self.factory.get(self.url)
        request.user = self.user1

        view = self.view_class()
        view.setup(request)

        with self.assertRaisesMessage(
            NotImplementedError, "Subclasses must implement get_results()"
        ):
            view.get_results()


class TestAllTablesResetView(BaseTestCase):
    url = reverse_lazy("results:reset-all")

    def setUp(self):
        self.client.force_login(self.user1)

    def test_redirect_anonymous_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse(settings.LOGIN_URL) + f"?next={self.url}",
        )

    def test_get(self):
        template_expected = "results/reset.html"
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_expected)

    def test_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("verbs:list"))
        self.assertFalse(Result.objects.filter(owner=self.user1.profile).exists())
        # Check that only user1 results are deleted
        self.assertTrue(Result.objects.filter(owner=self.user2.profile).exists())

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertRedirects(response, reverse("verbs:list"))
        self.assertFalse(Result.objects.filter(owner=self.user1.profile).exists())
        # Check that only user1 results are deleted
        self.assertTrue(Result.objects.filter(owner=self.user2.profile).exists())


class TestDefaultTableResetView(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.user1)
        self.url = reverse_lazy(
            "results:default:reset",
            kwargs={
                "pk": self.default_table.id,
                "slug_name": self.default_table.slug_name,
            },
        )

    def test_redirect_anonymous_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse(settings.LOGIN_URL) + f"?next={self.url}",
        )

    def test_get(self):
        template_expected = "results/reset.html"
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_expected)

    def test_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            reverse(
                "tables:default:detail",
                kwargs={
                    "pk": self.default_table.id,
                    "slug_name": self.default_table.slug_name,
                },
            ),
        )
        self.assertFalse(
            Result.objects.filter(
                owner=self.user1.profile,
                table=self.default_table,
            ).exists()
        )
        # UserTable results are not deleted
        self.assertTrue(
            Result.objects.filter(
                owner=self.user1.profile,
                table=self.user_table1,
            ).exists()
        )
        # Results from another user's DefaultTable are not deleted.
        self.assertTrue(
            Result.objects.filter(
                owner=self.user2.profile,
                table=self.default_table,
            ).exists()
        )

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertRedirects(
            response,
            reverse(
                "tables:default:detail",
                kwargs={
                    "pk": self.default_table.id,
                    "slug_name": self.default_table.slug_name,
                },
            ),
        )
        self.assertFalse(
            Result.objects.filter(
                owner=self.user1.profile,
                table=self.default_table,
            ).exists()
        )
        # UserTable results are not deleted
        self.assertTrue(
            Result.objects.filter(
                owner=self.user1.profile,
                table=self.user_table1,
            ).exists()
        )
        # Results from another user's DefaultTable are not deleted.
        self.assertTrue(
            Result.objects.filter(
                owner=self.user2.profile,
                table=self.default_table,
            ).exists()
        )


class TestUserTableResetView(BaseTestCase):
    def setUp(self):
        self.client.force_login(self.user1)
        self.url = reverse_lazy(
            "results:user:reset",
            kwargs={
                "pk": self.user_table1.id,
                "slug_name": self.user_table1.slug_name,
            },
        )

    def test_redirect_anonymous_user(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse(settings.LOGIN_URL) + f"?next={self.url}",
        )

    def test_get(self):
        template_expected = "results/reset.html"
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_expected)

    def test_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            reverse(
                "tables:user:detail",
                kwargs={
                    "pk": self.user_table1.id,
                    "slug_name": self.user_table1.slug_name,
                },
            ),
        )
        self.assertFalse(
            Result.objects.filter(
                owner=self.user1.profile,
                table=self.user_table1,
            ).exists()
        )
        # DefaultTable results are not deleted
        self.assertTrue(
            Result.objects.filter(
                owner=self.user1.profile,
                table=self.default_table,
            ).exists()
        )

    def test_delete(self):
        response = self.client.delete(self.url)
        self.assertRedirects(
            response,
            reverse(
                "tables:user:detail",
                kwargs={
                    "pk": self.user_table1.id,
                    "slug_name": self.user_table1.slug_name,
                },
            ),
        )
        self.assertFalse(
            Result.objects.filter(
                owner=self.user1.profile,
                table=self.user_table1,
            ).exists()
        )
        # DefaultTable results are not deleted
        self.assertTrue(
            Result.objects.filter(
                owner=self.user1.profile,
                table=self.default_table,
            ).exists()
        )
