from django.test import TestCase

from authentication.forms import DeleteAccountForm
from authentication.tests.fixtures import TestDataFixture


class TestDeleteAccountForm(TestDataFixture, TestCase):

    def test_form_raise_error_if_wrong_credential(self):
        data = {
            'email': 'wrong@email.com',
            'password': 'wrong password'
        }
        form = DeleteAccountForm(
            current_user=self.user,
            data=data
        )
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            None,
            [
                'Please enter a correct email and password. '
                'Note that both fields may be case-sensitive.'
            ]
        )
