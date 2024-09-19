from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class EmailBackend(ModelBackend):
    """
    Authenticates user with email address and password.
    Rejects inactive users.
    """
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None or password is None:
            return
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if (
                user.check_password(password)
                and self.user_can_authenticate(user)
            ):
                return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None


class AllowAllUsersEmailBackend(EmailBackend):
    """
    Authenticates user with email address and password.
    Allows inactive users.
    """
    def user_can_authenticate(self, user):
        return True
