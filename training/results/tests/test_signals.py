from django.contrib.auth import get_user_model
from django.test import TestCase

from training.results.models import Result
from training.tables.models import Table
from training.verbs.models import Verb


User = get_user_model()


class TestSignals(TestCase):
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
        cls.table.verbs.add(*[cls.verb1, cls.verb2])
        Result.objects.create(owner=cls.user.profile, table=cls.table, verb=cls.verb1)
        Result.objects.create(owner=cls.user.profile, table=cls.table, verb=cls.verb2)

    def test_delete_results(self):
        """
        The result should be deleted if the verb is removed from the
        table.
        """
        results_count = Result.objects.count()
        self.table.verbs.remove(self.verb1)
        self.assertEqual(Result.objects.count(), results_count - 1)
