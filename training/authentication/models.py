import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager
)


class MyUserManager(BaseUserManager):
    def _create_user(
        self,
        email,
        username,
        password
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

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)  # using default db

        return user

    def create_user(
        self,
        email,
        username,
        password,
    ):
        """
        Creates a user.
        """
        user = self._create_user(
            email=self.normalize_email(email),
            password=password,
            username=username
        )

        return user

    def create_superuser(
        self,
        email,
        username,
        password
    ):
        """
        Creates a superuser.
        """
        if not username:
            raise ValueError(
                'Users must have a username.'
            )

        admin_username = '[admin]' + username
        user = self._create_user(
            email,
            username=admin_username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4
    )
    email = models.EmailField(
        max_length=62,
        unique=True
    )
    last_update = models.DateField(
        auto_now=True
    )

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
    ]

    def __str__(self):
        return self.username
