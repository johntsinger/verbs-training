from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from training.results.models import Result
from training.tables.models import Table
from training.verbs.models import Verb


User = get_user_model()


class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user",
            email="user@email.com",
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
        cls.table = Table.objects.create(name="test", owner=cls.user.profile)
        cls.table.verbs.add(*[cls.verb1])


class TestResultManager(BaseTestCase):
    def test_create_missing_profile(self):
        with self.assertRaisesMessage(ValueError, "Result must have an owner"):
            Result.objects.create(
                owner="",
                table=self.table,
                verb=self.verb2,
            )

    def test_create_missing_table(self):
        with self.assertRaisesMessage(ValueError, "Result must have a table"):
            Result.objects.create(
                owner=self.user.profile,
                table="",
                verb=self.verb2,
            )

    def test_create_missing_verb(self):
        with self.assertRaisesMessage(ValueError, "Result must have a verb"):
            Result.objects.create(
                owner=self.user.profile,
                table=self.table,
                verb="",
            )


class TestResultModel(BaseTestCase):
    def test_str(self):
        expected = (
            "Result: "
            f"owner <{self.user.profile}> "
            f"table <{self.table}> "
            f"verb <{self.verb1.infinitive}>"
        )
        result = Result.objects.create(
            owner=self.user.profile, table=self.table, verb=self.verb1
        )
        self.assertEqual(str(result), expected)

    def test_unique_constraint(self):
        Result.objects.create(
            owner=self.user.profile, table=self.table, verb=self.verb1
        )
        with self.assertRaises(IntegrityError):
            Result.objects.create(
                owner=self.user.profile, table=self.table, verb=self.verb1
            )

    def test_create_result_verb_not_belong_to_table_raise_error(self):
        with self.assertRaisesMessage(
            ValidationError,
            f"The verb '{self.verb2}' does not belong to '{self.table}' table.",
        ):
            Result.objects.create(
                owner=self.user.profile,
                table=self.table,
                verb=self.verb2,
            )

    def test_create_result_usertable_not_belong_to_profile_raise_error(self):
        user2 = User.objects.create_user(
            username="user2",
            email="user2@email.com",
            password="password",
        )
        with self.assertRaisesMessage(
            ValidationError,
            f"The table '{self.table}' does not belong to '{user2.profile} profile",
        ):
            Result.objects.create(
                owner=user2.profile,
                table=self.table,
                verb=self.verb1,
            )
