# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import AnonymousUser
# from django.test import TestCase  # override_settings
# from django.urls import reverse_lazy

# from training.common.testcase.mixins import RequestFactoryMixin
# from training.results.models import Result
# from training.tables.models import DefaultTable
# from training.verbs.models import Verb, Similarity, Info, Example
# from training.verbs.views import VerbListView


# User = get_user_model()


# class TestDataMixin:

#     @classmethod
#     def setUpTestData(cls):
#         cls.user = User.objects.create_user(
#             email='user@email.com',
#             password='password',
#             username='username'
#         )
#         cls.similarity = Similarity.objects.create(
#             name='similarity name'
#         )
#         cls.verb = Verb.objects.create(
#             infinitive='begin',
#             simple_past='began',
#             past_participle='begun',
#             translation='commencer',
#             similarity=cls.similarity
#         )
#         cls.info = Info.objects.create(
#             content='info content',
#             verb=cls.verb
#         )
#         cls.example = Example.objects.create(
#             english='example english',
#             translation='example translation',
#             verb=cls.verb
#         )
#         cls.default_table = DefaultTable.objects.create(
#             name='default table name'
#         )
#         cls.default_table.verbs.add(cls.verb)
#         cls.result = Result.objects.create(
#             verb=cls.verb,
#             profile=cls.user.profile,
#             table=cls.default_table,
#             is_success=True
#         )


# class TestVerbsViews(
#     TestDataMixin,
#     RequestFactoryMixin,
#     TestCase
# ):
#     view_class = VerbListView
#     url = reverse_lazy('verbs-list')

#     def test_get_queryset_anonymous_user(self):
#         """
#         Test that get_queryset does not return a queryset annotated
#         with the result (is_success) for an anonymous user.
#         """
#         request = self.factory.get(self.url)
#         request.user = AnonymousUser()
#         view = self.view_class()
#         view.setup(request)
#         queryset = view.get_queryset()

#         with self.assertRaises(AttributeError):
#             queryset.first().is_success

#     def test_get_queryset_authenticated_user(self):
#         """
#         Test that get_queryset returns a queryset annotated
#         with the result (is_success) for an authenticated user.
#         """
#         request = self.factory.get(self.url)
#         request.user = self.user
#         view = self.view_class()
#         view.setup(request)
#         queryset = view.get_queryset()

#         self.assertTrue(queryset.first().is_success)
