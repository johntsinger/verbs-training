from django.contrib.auth import get_user_model

from results.models import Result
from tables.models import DefaultTable
from verbs.models import Verb, Similarity, Info, Example


User = get_user_model()


class TestDataFixture:

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='user@email.com',
            password='password',
            username='username'
        )
        cls.similarity = Similarity.objects.create(
            name='similarity name'
        )
        cls.verb = Verb.objects.create(
            infinitive='begin',
            simple_past='began',
            past_participle='begun',
            translation='commencer',
            similarity=cls.similarity
        )
        cls.info = Info.objects.create(
            content='info content',
            verb=cls.verb
        )
        cls.example = Example.objects.create(
            english='example english',
            translation='example translation',
            verb=cls.verb
        )
        cls.default_table = DefaultTable.objects.create(
            name='default table name'
        )
        cls.default_table.verbs.add(cls.verb)
        cls.result = Result.objects.create(
            verb=cls.verb,
            profile=cls.user.profile,
            table=cls.default_table,
            is_success=True
        )
