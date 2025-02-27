from django.test import TestCase

from training.verbs.models import Example, Info, Similarity, Verb


class TestVerbModel(TestCase):
    def test_str(self):
        verb = Verb.objects.create(
            infinitive="begin",
            simple_past="began",
            past_participle="begun",
            translation="commencer",
        )
        expected = (
            f"{verb.infinitive} {verb.simple_past} {verb.past_participle} "
            f"{verb.translation}"
        )
        self.assertEqual(str(verb), expected)


class TestSimilarityModel(TestCase):
    def test_str(self):
        similarity = Similarity.objects.create(name="similarity name")
        expected = f"{similarity.name}"
        self.assertEqual(str(similarity), expected)


class TestInfoModel(TestCase):
    def test_str(self):
        verb = Verb.objects.create(
            infinitive="begin",
            simple_past="began",
            past_participle="begun",
            translation="commencer",
        )
        info = Info.objects.create(content="info content", verb=verb)
        expected = f"Info for verb {verb.infinitive}"
        self.assertEqual(str(info), expected)


class TestExampleModel(TestCase):
    def test_str(self):
        verb = Verb.objects.create(
            infinitive="begin",
            simple_past="began",
            past_participle="begun",
            translation="commencer",
        )
        example = Example.objects.create(
            english="example english", translation="example translation", verb=verb
        )
        expected = f"Example for verb {verb.infinitive}"
        self.assertEqual(str(example), expected)
