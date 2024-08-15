from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class TestUserManager(TestCase):

    def missing_email_message(self):
        return 'Users must have an email address.'

    def missing_username_message(self):
        return 'Users must have a username.'

    def missing_password_message(self):
        return 'Users must have a password.'

    def test_create_user(self):
        user_count = User.objects.count()
        user = User.objects.create_user(
            email='user@email.com',
            username='username',
            password='password'
        )
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user_count + 1, User.objects.count())
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_user_missing_email(self):
        with self.assertRaises(
            ValueError,
            msg=self.missing_email_message()
        ):
            User.objects.create_user(
                email='',
                username='username',
                password='password'
            )

    def test_create_user_missing_username(self):
        with self.assertRaises(
            ValueError,
            msg=self.missing_username_message()
        ):
            User.objects.create_user(
                email='user@email.com',
                username='',
                password='password'
            )

    def test_create_user_missing_password(self):
        with self.assertRaises(
            ValueError,
            msg=self.missing_password_message()
        ):
            User.objects.create_user(
                email='user@email.com',
                username='username',
                password=''
            )

    def test_create_superuser(self):
        user_count = User.objects.count()
        superuser = User.objects.create_superuser(
            email='superuser@email.com',
            username='username',
            password='password'
        )
        self.assertTrue(isinstance(superuser, User))
        self.assertEqual(user_count + 1, User.objects.count())
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_create_superuser_missing_email(self):
        with self.assertRaises(
            ValueError,
            msg=self.missing_email_message()
        ):
            User.objects.create_superuser(
                email='',
                username='username',
                password='password'
            )

    def test_create_superuser_missing_username(self):
        with self.assertRaises(
            ValueError,
            msg=self.missing_username_message()
        ):
            User.objects.create_superuser(
                email='superuser@email.com',
                username='',
                password='password'
            )

    def test_create_superuser_missing_password(self):
        with self.assertRaises(
            ValueError,
            msg=self.missing_password_message()
        ):
            User.objects.create_superuser(
                email='superuser@email.com',
                username='username',
                password=''
            )


class TestUserModels(TestCase):

    def test_user_str(self):
        user = User.objects.create_user(
            email='user@email.com',
            username='username',
            password='password'
        )
        self.assertEqual(str(user), 'username')

    def test_superuser_str(self):
        superuser = User.objects.create_superuser(
            email='superuser@email.com',
            username='username',
            password='password'
        )
        self.assertEqual(str(superuser), 'username')
