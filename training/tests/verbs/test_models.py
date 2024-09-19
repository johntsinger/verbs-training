from django.test import TestCase
from verbs.models import Verb, Similarity, Info, Example


class TestModels(TestCase):

    @classmethod
    def setUpTestData(cls):
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

    def test_verb_str(self):
        expected = 'begin began begun commencer'
        self.assertEqual(str(self.verb), expected)

    def test_similarity_str(self):
        expected = 'similarity name'
        self.assertEqual(str(self.similarity), expected)

    def test_info_str(self):
        expected = 'Info for verb begin'
        self.assertEqual(str(self.info), expected)

    def test_example_str(self):
        expected = 'Example for verb begin'
        self.assertEqual(str(self.example), expected)
