
import binascii
import hashlib
import os
import sqlite3

from .User import AuthMethodEnum, User


class UserManager:
    """A very simple User Manager, that manages `User` objects and writes them to database"""

    def __init__(self, db: sqlite3.Connection):
        """Create UserManager object

        # Args:
            - db (sqlite3.Connection): preexisting sqlite3 connection object
        """
        self.db = db
        self.db.row_factory = sqlite3.Row

    def login(self, username: str, password: str):
        """Logins in a user after username and password have been validated

        Args:
            username (String): username
            password (String): password

        Returns:
            bool: ``User`` on success, else False
        """
        user = self.get_user(username)

        # user does not exist
        if user is None:
            return False

        if not self.check_password(user, password):
            return False

        # authenticated set to true
        user.authenticated = True

        # authenticated update
        if not self.update(user):
            return False

        return user

    def logout(self, user: User) -> bool:
        """Logs out the current user

        Returns:
            bool: ``True`` on success, else False
        """
        user.authenticated = False
        return self.update(user)

    def register(self, user: 'User'):
        """Creates a new user and authenticates a new user after username and password are validated

        Args:
            user (User): User object


        Returns:
            bool: ``True`` on success, else False
        """
        if self.add_user(user):
            return self.login(user.username, user.password)

        return False

    def unregister(self, user: User) -> bool:
        """Deletes current user's profile

        Returns:
            bool: ``True`` on success, else False
        """
        return self.delete_user(user.get_id())

    def add_user(self, user: 'User'):
        """Creates new user in the database

        Args:
            user (User): User object

        Returns:
            user on success, False otherwise
        """
        cur = self.db.execute(
            'select * from users where username = ?',
            (user.username,)
        )

        result = cur.fetchall()

        # user already exists
        if result:
            return False

        if user.authentication_method == AuthMethodEnum.HASH:
            user.hash = make_salted_hash(user.password)

        self.db.execute(
            'insert into users (username, active, authentication_method, password, hash, authenticated, roles) values (?, ?, ?, ?, ?, ?, ?)',
            (
                # The following are to be stored in the sqlite database.
                # Any booleans will have to be stored as integers since
                # sqlite does not support the boolean datatype.

                # username is intended to be store as text and will be the key that
                # all entries are indexed by.
                user.username,

                # active will mark whether the user account is active.
                # It will be stored in sqlite as an int
                user.active,

                # Our authentication methods(not to be confused with Python methods)
                # are identified by an int and that will be how we store them in the
                # sqlite database.
                user.authentication_method.value,

                # This is the user's password.  It'll be stored as a text value.
                user.password,

                # If the password is hased, this will hold the result.
                # Also stored as text.
                user.hash,
                user.authenticated,
                " ".join(user.roles)
            )
        )
        self.db.commit()
        return user

    def get_user(self, username: str):
        """Get `User` from the database

        # Args:
            - name (str): users name
        # Returns:
            - User | None: User object if user with the given username is found, otherwise nothing is returned.
        """
        cur = self.db.execute(
            'select * from users where username = ?',
            (username,)
        )
        user = cur.fetchone()
        if not user:
            return None
        return User.from_dict(user)

    def delete_user(self, username: str) -> bool:
        """Deletes user from the database

        Args:
            name (str): users username

        Returns:
            bool: True if delete was successful, otherwise False
        """
        # https://stackoverflow.com/questions/13313694/how-do-i-determine-if-the-row-has-been-inserted
        try:
            self.db.execute(
                'delete from users where username = ?',
                (username,)
            )
            self.db.commit()
            return True
        except sqlite3.Error:
            return False

    def update(self, user: 'User') -> bool:
        """Update user from userdata dictionary

        Args:
            user (User): user to delete

        Returns:
            bool: True if delete was successful, otherwise False
        """
        try:
            self.db.execute(
                'update users set active = ?, password = ?, authenticated = ? where username = ?',
                (
                    user.active,
                    user.password,
                    user.authenticated,
                    user.username
                )
            )

            self.db.commit()
            return True
        except sqlite3.Error:
            return False

    @staticmethod
    def check_password(user: User, password: str) -> bool:
        """Check if user password matches the password in the database

        Args:
            user ('User'): user object
            password (str): user password

        Returns:
            bool: did password match
        """

        authentication_method = user.authentication_method
        result = False

        if authentication_method is AuthMethodEnum.HASH.value:
            result = check_hashed_password(password, user.password)

        elif authentication_method is AuthMethodEnum.CLEARTEXT.value:
            result = (user.password == password)

        return result


def make_salted_hash(password, salt=None):
    if not salt:
        salt = os.urandom(64)
    d = hashlib.sha512()
    d.update(salt[:32])
    d.update(password)
    d.update(salt[32:])
    return str(binascii.hexlify(salt)) + d.hexdigest()


def check_hashed_password(password, salted_hash):
    salt = binascii.unhexlify(salted_hash[:128])
    return make_salted_hash(password, salt) == salted_hash
