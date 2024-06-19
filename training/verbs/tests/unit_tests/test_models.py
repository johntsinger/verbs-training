from django.test import TestCase
from verbs.models import Verb, Similarity, Info, Example


class TestModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.similarity = Similarity.objects.create(
            name="similarity name"
        )
        cls.verb = Verb.objects.create(
            infinitive="verb infinitive",
            simple_past="verb simple past",
            past_participle="verb past participle",
            translation="verb translation",
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

    def test_verb_str(self):
        expected = ""