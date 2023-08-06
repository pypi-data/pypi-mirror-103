from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class AuthMethodEnum(Enum):
    """Enum that stores supported authentication methods
    """
    CLEARTEXT = 0
    HASH = 1


@dataclass
class User:
    """Represents User entry in the sqlite3 database

    Variables: 
        * username (str): The user's name.  Used as the primary key in the database.
        * password (str): The user's password.  Stored as text in sqlite.
        * roles (str): The roles a user has.  It's a list of string, but will be
            stored as a single text value in sqlite.
        * authentication_method (int): Used to reference an authentication
            method by number.
        * authenticated (bool): Flag for whether a user has been authenticated.
            Stored in sqlite as an int.
        * hash (str): Stored result if password has been hashed.
        * anonymous (bool): Flag for anonymous users.  Since a registered user is 
            not anonymous, this is not stored in sqlite.
    """
    username: str
    password: str

    active: bool = field(default=True)
    roles: List[str] = field(default_factory=list)
    authentication_method: AuthMethodEnum = field(
        default=AuthMethodEnum.CLEARTEXT)
    authenticated: bool = field(default=False)
    hash: str = field(default="")
    anonymous: bool = field(default=False)

    def is_authenticated(self):
        """Returns whether the User is authenticated.

        Args:
        self (int): The current instance of User

        Returns:
        bool:authentication state

        """
        return self.authenticated

    def is_active(self):
        """Returns whether the User is active. Required by flask-login.

        Args:
        self (int): The current instance of User

        Returns:
        bool:active state

        """
        return self.is_active

    def is_anonymous(self):
        """Returns whether the User is anonymous.  In this case, all users are not.

        Args:
        self (int): The current instance of User

        Returns:
        bool:anonymous state


        """
        return self.anonymous

    def get_id(self):
        """Returns the username of a user. Required by flask-login.

        Args:
        self (int): The current instance of User

        Returns:
        str:username

        """
        return self.username

    @staticmethod
    def from_dict(user: Dict[str, Any]) -> 'User':
        """converts array of sql data into dictionary

        Args:
            user (List[str]): sql array of data

        Returns:
            Dict[str, Any]: Dictionary of values
        """

        roles = user["roles"].split()
        return User(username=user["username"],
                    password=user["password"],
                    hash=user["hash"],
                    active=user["active"],
                    roles=roles,
                    authentication_method=user["authentication_method"],
                    authenticated=user["authenticated"])
