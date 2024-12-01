import uuid

from django.apps import apps
from django.contrib import auth
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager
)
from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _


class MyUserManager(BaseUserManager):
    def _create_user(
        self,
        username,
        email,
        password,
        **extra_fields
    ):
        """
        Creates and saves a User with the given email, password and username.
        """
        if not email:
            raise ValueError(
                'Users must have an email address.'
            )

        if not username:
            raise ValueError(
                'Users must have a username.'
            )

        if not password:
            raise ValueError(
                'Users must have a password.'
            )

        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        email = self.normalize_email(email)
        username = GlobalUserModel.normalize_username(username)

        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)  # using default db

        return user

    def create_user(
        self,
        username,
        email,
        password,
        **extra_fields
    ):
        """
        Creates a user.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(
        self,
        username,
        email,
        password,
        **extra_fields
    ):
        """
        Creates a superuser.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

    def with_perm(
        self,
        perm,
        is_active=True,
        include_superusers=True,
        backend=None,
        obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4
    )
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': _('A user with that email already exists.'),
        }
    )
    updated_at = models.DateField(
        verbose_name=_('updated at'),
        auto_now=True
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('email'),
                name='case_insensitive_unique_user_email',
            ),
        ]

    def clean(self):
        self.username = self.normalize_username(self.username)
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self):
        return self.username
