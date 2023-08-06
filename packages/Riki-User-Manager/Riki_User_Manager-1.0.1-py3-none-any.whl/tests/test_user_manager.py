import unittest
import sqlite3
from riki_usermanager import AuthMethodEnum, UserManager, User
from faker import Faker
from pathlib import Path


class TestUserManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        new_db = sqlite3.connect(':memory:')  # create a memory database
        new_db.executescript(Path('schema.sql').read_text())
        cls.faker = Faker()

        profile = cls.faker.profile()

        new_db.execute(
            'insert into users (username, active, authentication_method, password, hash, authenticated, roles) values (?, ?, ?, ?, ?, ?, ?)',
            (profile['username'], True, 0,
             cls.faker.password(), '', False, '', )
        )

        cls.existing_profile = profile
        cls.user_manager = UserManager(new_db)

    def test_add_new_user(self):
        profile = self.faker.profile()
        password = self.faker.password()

        user = User(profile['username'], password=password,
                    active=True, authentication_method=AuthMethodEnum.CLEARTEXT)

        self.assertTrue(self.user_manager.add_user(user))
        self.assertEqual(user.username, profile['username'])
        self.assertEqual(user.authentication_method, AuthMethodEnum.CLEARTEXT)
        self.assertFalse(self.user_manager.add_user(user))

    def test_delete_user(self):
        profile = self.faker.profile()
        password = self.faker.password()

        user = User(profile['username'], password=password,
                    active=True, authentication_method=AuthMethodEnum.CLEARTEXT)

        self.assertTrue(self.user_manager.add_user(user))
        self.assertTrue(self.user_manager.delete_user(user.username))

    def test_get_existing_user(self):
        profile = self.existing_profile
        user = self.user_manager.get_user(profile['username'])

        self.assertEqual(user.username, profile['username'])

    def test_get_nonexisting_user(self):
        profile = self.faker.profile()
        user = self.user_manager.get_user(profile['username'])

        self.assertIsNone(user)

    def test_update_user(self):
        profile = self.faker.profile()
        new_profile = self.faker.profile()
        password = self.faker.password()
        new_password = self.faker.password()

        user = User(profile['username'], password=password,
                    active=True, authentication_method=AuthMethodEnum.CLEARTEXT)
        updated_user = User(profile['username'], password=password,
                            active=False, authentication_method=AuthMethodEnum.CLEARTEXT)
        self.user_manager.add_user(user)

        self.assertTrue(self.user_manager.update(updated_user))

        user = self.user_manager.get_user(profile['username'])
        self.assertFalse(user.active)
