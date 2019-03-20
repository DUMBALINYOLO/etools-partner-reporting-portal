from faker import Faker

from core.factories import (
    PartnerUserFactory,
    PartnerFactory,
)
from core.tests.base import BaseAPITestCase

from account.forms import (
    CustomUserCreationForm,
    UserAdminForm,
)


class CustomUserCreationFormTestcase(BaseAPITestCase):

    def setUp(self):
        super().setUp()
        self.faker = Faker()

    def test_valid_submission(self):
        """Test if the form is filled correctly
        """
        form = CustomUserCreationForm(data={
            'username': self.faker.user_name(),
            'first_name': self.faker.first_name(),
            'last_name': self.faker.last_name(),
            'email': self.faker.ascii_safe_email(),
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertTrue(form.is_valid())

    def test_required_fields(self):
        """Test if the form throws an error by requiring username and email fields.
        """
        form = CustomUserCreationForm(data={
            'first_name': self.faker.first_name(),
            'last_name': self.faker.last_name(),
        })
        self.assertFalse(form.is_valid())


class UserAdminFormTestcase(BaseAPITestCase):

    def setUp(self):
        self.partner = PartnerFactory()
        self.user = PartnerUserFactory(partner=self.partner)

        super().setUp()
        self.faker = Faker()

    def test_valid_submission(self):
        """Test if the form is filled correctly
        """
        form = UserAdminForm(data={
            'first_name': self.faker.first_name(),
            'last_name': self.faker.last_name(),
            'username': self.user.username,
            'email': self.user.email,
            'password1': 'testpassword',
            'password2': 'testpassword',
            'partner': self.partner.id,
            'organization': None,
        }, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_organization_field_handling(self):
        """Test if the form throws an error if the form has no partner or no organization
        """
        form = UserAdminForm(data={
            'first_name': self.faker.first_name(),
            'last_name': self.faker.last_name(),
            'username': self.user.username,
            'email': self.user.email,
            'password1': 'testpassword',
            'password2': 'testpassword',
            'partner': None,
            'organization': None,
        }, instance=self.user)
        self.assertFalse(form.is_valid())