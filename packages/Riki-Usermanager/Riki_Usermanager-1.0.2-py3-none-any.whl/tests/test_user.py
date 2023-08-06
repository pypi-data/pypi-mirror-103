from unittest import TestCase
from riki_usermanager import User
from faker import Faker


class TestUser(TestCase):
    def setUp(self) -> None:
        faker = Faker()
        self.username = faker.profile()['username']

        self.user = User(self.username, faker.password(), active=False)
        return super().setUp()

    def test_User__is_authenticated(self):
        self.assertFalse(self.user.is_authenticated())

    def test_User__is_active(self):
        self.assertTrue(self.user.is_active())

    def test_User__is_anonymous(self):
        self.assertFalse(self.user.is_anonymous())

    def test_User__get_id(self):
        self.assertEqual(self.user.get_id(), self.username)

    def test_User__from_dict(self):
        user_dict = {
            "username": self.user.username,
            "password": self.user.password,
            "hash": self.user.hash,
            "active": self.user.active,
            "roles": " ".join(self.user.roles),
            "authentication_method": self.user.authentication_method,
            "authenticated": self.user.authenticated
        }

        self.assertEqual(User.from_dict(user_dict), self.user)
