from django.contrib.auth import get_user_model
from django.test import TestCase

from training.profiles.models import Profile


User = get_user_model()


class BaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user",
            email="user@email.com",
            password="password",
        )


class ProfileModelTests(BaseTestCase):
    def test_str(self):
        profile = Profile.objects.get()
        self.assertEqual(str(profile), self.user.username)
