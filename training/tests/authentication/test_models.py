from django.contrib.auth.models import (
    Group,
    Permission
)
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from authentication.backends import EmailBackend


User = get_user_model()


class TestUserManager(TestCase):

    def test_create_user(self):
        user_count = User.objects.count()
        user_data = {
            'username': 'user',
            'email': 'user@email.com',
            'password': 'password'
        }
        user = User.objects.create_user(**user_data)
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.username, user_data['username'])
        self.assertEqual(user.email, user_data['email'])
        self.assertTrue(user.check_password(user_data['password']))
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertEqual(user_count + 1, User.objects.count())

    def test_create_user_is_staff(self):
        user = User.objects.create_user(
            username='user',
            email='user@email.com',
            password='password',
            is_staff=True
        )
        self.assertTrue(user.is_staff)

    def test_create_user_normalize_email_domain(self):
        uppercase_email_domain = 'user@EMAIL.COM'
        expected_email = 'user@email.com'
        user = User.objects.create_user(
            username='user',
            email=uppercase_email_domain,
            password='password'
        )
        self.assertEqual(user.email, expected_email)

    def test_create_user_normalize_username(self):
        ohm_username = 'testΩ'  # U+2126 OHM SIGN
        expected_username = 'testΩ'  # U+03A9 GREEK CAPITAL LETTER OMEGA
        user = User.objects.create_user(
            username=ohm_username,
            email='user@EMAIL.COM',
            password='password'
        )
        self.assertNotEqual(user.username, ohm_username)
        self.assertEqual(user.username, expected_username)

    def test_create_user_missing_email(self):
        with self.assertRaises(
            ValueError,
            msg='Users must have an email address.'
        ):
            User.objects.create_user(
                username='user',
                email='',
                password='password'
            )

    def test_create_user_missing_username(self):
        with self.assertRaises(
            ValueError,
            msg='Users must have a username.'
        ):
            User.objects.create_user(
                username='',
                email='user@email.com',
                password='password'
            )

    def test_create_user_missing_password(self):
        with self.assertRaises(
            ValueError,
            msg='Users must have a password.'
        ):
            User.objects.create_user(
                username='user',
                email='user@email.com',
                password=''
            )

    def test_create_superuser(self):
        user_count = User.objects.count()
        superuser = User.objects.create_superuser(
            username='superuser',
            email='superuser@email.com',
            password='password'
        )
        self.assertTrue(isinstance(superuser, User))
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertEqual(user_count + 1, User.objects.count())

    def test_create_super_user_raises_error_on_false_is_superuser(self):
        with self.assertRaisesMessage(
            ValueError,
            'Superuser must have is_superuser=True.'
        ):
            User.objects.create_superuser(
                username='superuser',
                email='superuser@email.com',
                password='password',
                is_superuser=False,
            )

    def test_create_superuser_raises_error_on_false_is_staff(self):
        with self.assertRaisesMessage(
            ValueError,
            'Superuser must have is_staff=True.'
        ):
            User.objects.create_superuser(
                username='superuser',
                email='superuser@email.com',
                password='password',
                is_staff=False,
            )


class CustomModelBackend(EmailBackend):
    def with_perm(
        self,
        perm,
        is_active=True,
        include_superusers=True,
        backend=None,
        obj=None
    ):
        if obj is not None and obj.username == 'charliebrown':
            return User.objects.filter(pk=obj.pk)
        return User.objects.filter(username__startswith='charlie')


@override_settings(
    AUTHENTICATION_BACKENDS=['authentication.backends.EmailBackend']
)
class UserWithPermTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        content_type = ContentType.objects.get_for_model(Group)
        cls.permission = Permission.objects.create(
            name='test',
            content_type=content_type,
            codename='test',
        )
        # User with permission.
        cls.user1 = User.objects.create_user(
            'user 1', 'foo@example.com', 'password'
        )
        cls.user1.user_permissions.add(cls.permission)
        # User with group permission.
        group1 = Group.objects.create(name='group 1')
        group1.permissions.add(cls.permission)
        group2 = Group.objects.create(name='group 2')
        group2.permissions.add(cls.permission)
        cls.user2 = User.objects.create_user(
            'user 2', 'bar@example.com', 'password'
        )
        cls.user2.groups.add(group1, group2)
        # Users without permissions.
        cls.user_charlie = User.objects.create_user(
            'charlie', 'charlie@example.com', 'password'
        )
        cls.user_charlie_b = User.objects.create_user(
            'charliebrown', 'charlie@brown.com', 'password'
        )
        # Superuser.
        cls.superuser = User.objects.create_superuser(
            'superuser',
            'superuser@example.com',
            'superpassword',
        )
        # Inactive user with permission.
        cls.inactive_user = User.objects.create_user(
            'inactive_user',
            'baz@example.com',
            'password',
            is_active=False,
        )
        cls.inactive_user.user_permissions.add(cls.permission)

    def test_invalid_permission_name(self):
        msg = (
            'Permission name should be in the '
            'form app_label.permission_codename.'
        )
        for perm in ('nodots', 'too.many.dots', '...', ''):
            with self.subTest(perm), self.assertRaisesMessage(ValueError, msg):
                User.objects.with_perm(perm)

    def test_invalid_permission_type(self):
        msg = 'The `perm` argument must be a string or a permission instance.'
        for perm in (b'auth.test', object(), None):
            with self.subTest(perm), self.assertRaisesMessage(TypeError, msg):
                User.objects.with_perm(perm)

    def test_invalid_backend_type(self):
        msg = 'backend must be a dotted import path string (got %r).'
        for backend in (b'auth_tests.CustomModelBackend', object()):
            with self.subTest(backend):
                with self.assertRaisesMessage(TypeError, msg % backend):
                    User.objects.with_perm('auth.test', backend=backend)

    def test_basic(self):
        active_users = [self.user1, self.user2]
        tests = [
            ({}, [*active_users, self.superuser]),
            ({'obj': self.user1}, []),
            # Only inactive users.
            ({'is_active': False}, [self.inactive_user]),
            # All users.
            (
                {'is_active': None},
                [*active_users, self.superuser, self.inactive_user]
            ),
            # Exclude superusers.
            ({'include_superusers': False}, active_users),
            (
                {'include_superusers': False, 'is_active': False},
                [self.inactive_user],
            ),
            (
                {'include_superusers': False, 'is_active': None},
                [*active_users, self.inactive_user],
            ),
        ]
        for kwargs, expected_users in tests:
            for perm in ('auth.test', self.permission):
                with self.subTest(perm=perm, **kwargs):
                    self.assertCountEqual(
                        User.objects.with_perm(perm, **kwargs),
                        expected_users,
                    )

    @override_settings(
        AUTHENTICATION_BACKENDS=['django.contrib.auth.backends.BaseBackend']
    )
    def test_backend_without_with_perm(self):
        self.assertSequenceEqual(User.objects.with_perm('auth.test'), [])

    def test_nonexistent_permission(self):
        self.assertSequenceEqual(
            User.objects.with_perm('auth.perm'),
            [self.superuser]
        )

    def test_nonexistent_backend(self):
        with self.assertRaises(ImportError):
            User.objects.with_perm(
                'auth.test',
                backend='invalid.backend.CustomModelBackend',
            )

    def test_invalid_backend_submodule(self):
        with self.assertRaises(ImportError):
            User.objects.with_perm(
                'auth.test',
                backend='json.tool',
            )

    @override_settings(
        AUTHENTICATION_BACKENDS=[
            'tests.authentication.test_models.CustomModelBackend'
        ]
    )
    def test_custom_backend(self):
        for perm in ('auth.test', self.permission):
            with self.subTest(perm):
                self.assertCountEqual(
                    User.objects.with_perm(perm),
                    [self.user_charlie, self.user_charlie_b],
                )

    @override_settings(
        AUTHENTICATION_BACKENDS=[
            'tests.authentication.test_models.CustomModelBackend'
        ]
    )
    def test_custom_backend_pass_obj(self):
        for perm in ('auth.test', self.permission):
            with self.subTest(perm):
                self.assertSequenceEqual(
                    User.objects.with_perm(perm, obj=self.user_charlie_b),
                    [self.user_charlie_b],
                )

    @override_settings(
        AUTHENTICATION_BACKENDS=[
            'tests.authentication.test_models.CustomModelBackend',
            'django.contrib.auth.backends.ModelBackend',
        ]
    )
    def test_multiple_backends(self):
        msg = (
            'You have multiple authentication backends configured and '
            'therefore must provide the `backend` argument.'
        )
        with self.assertRaisesMessage(ValueError, msg):
            User.objects.with_perm('auth.test')

        backend = (
            'tests.authentication.test_models.CustomModelBackend'
        )
        self.assertCountEqual(
            User.objects.with_perm('auth.test', backend=backend),
            [self.user_charlie, self.user_charlie_b],
        )


class TestUserModels(TestCase):

    def test_user_str(self):
        user = User.objects.create_user(
            username='user',
            email='user@email.com',
            password='password'
        )
        self.assertEqual(str(user), 'user')

    def test_superuser_str(self):
        superuser = User.objects.create_superuser(
            username='superuser',
            email='superuser@email.com',
            password='password'
        )
        self.assertEqual(str(superuser), 'superuser')
