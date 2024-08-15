from django.contrib.auth import get_user_model


User = get_user_model()


class TestDataFixture:
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='user@email.com',
            username='username',
            password='password'
        )
