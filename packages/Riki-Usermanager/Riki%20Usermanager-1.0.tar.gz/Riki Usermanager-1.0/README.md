# Riki UserManager

Classes for handling user CRUD and login/logout for CSC485 project.

<a name="riki_usermanager"></a>
# riki\_usermanager

<a name="riki_usermanager.User"></a>
# riki\_usermanager.User

<a name="riki_usermanager.User.AuthMethodEnum"></a>
## AuthMethodEnum Objects

```python
class AuthMethodEnum(Enum)
```

Enum that stores supported authentication methods

<a name="riki_usermanager.User.User"></a>
## User Objects

```python
@dataclass
class User()
```

Represents User entry in the sqlite3 database

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

<a name="riki_usermanager.User.User.is_authenticated"></a>
#### is\_authenticated

```python
 | is_authenticated()
```

Returns whether the User is authenticated.

**Arguments**:

- `self` _int_ - The current instance of User
  

**Returns**:

  bool:authentication state

<a name="riki_usermanager.User.User.is_active"></a>
#### is\_active

```python
 | is_active()
```

Returns whether the User is active. Required by flask-login.

**Arguments**:

- `self` _int_ - The current instance of User
  

**Returns**:

  bool:active state

<a name="riki_usermanager.User.User.is_anonymous"></a>
#### is\_anonymous

```python
 | is_anonymous()
```

Returns whether the User is anonymous.  In this case, all users are not.

**Arguments**:

- `self` _int_ - The current instance of User
  

**Returns**:

  bool:anonymous state

<a name="riki_usermanager.User.User.get_id"></a>
#### get\_id

```python
 | get_id()
```

Returns the username of a user. Required by flask-login.

**Arguments**:

- `self` _int_ - The current instance of User
  

**Returns**:

  str:username

<a name="riki_usermanager.User.User.from_dict"></a>
#### from\_dict

```python
 | @staticmethod
 | from_dict(user: Dict[str, Any]) -> 'User'
```

converts array of sql data into dictionary

**Arguments**:

- `data` _List[str]_ - sql array of data
  

**Returns**:

  Dict[str, Any]: Dictionary of values

<a name="riki_usermanager.UserManager"></a>
# riki\_usermanager.UserManager

<a name="riki_usermanager.UserManager.UserManager"></a>
## UserManager Objects

```python
class UserManager()
```

A very simple User Manager, that manages `User` objects and writes them to database

<a name="riki_usermanager.UserManager.UserManager.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(db: sqlite3.Connection)
```

Create UserManager object

# Args:
- db (sqlite3.Connection): preexisting sqlite3 connection object

<a name="riki_usermanager.UserManager.UserManager.login"></a>
#### login

```python
 | login(username: str, password: str) -> Union[User, Literal[False]]
```

Logins in a user after username and password have been validated

**Arguments**:

- `username` _String_ - username
  

**Returns**:

- `bool` - ``True`` on success, else False

<a name="riki_usermanager.UserManager.UserManager.logout"></a>
#### logout

```python
 | logout(user: User) -> bool
```

Logs out the current user

**Returns**:

- `bool` - ``True`` on success, else False

<a name="riki_usermanager.UserManager.UserManager.register"></a>
#### register

```python
 | register(user: 'User') -> Union['User', Literal[False]]
```

Creates a new user and authenticates a new user after username and password are validated

**Arguments**:

- `user` _User_ - User object
  
  

**Returns**:

- `bool` - ``True`` on success, else False

<a name="riki_usermanager.UserManager.UserManager.unregister"></a>
#### unregister

```python
 | unregister(user: User) -> bool
```

Deletes current user's profile

**Returns**:

- `bool` - ``True`` on success, else False

<a name="riki_usermanager.UserManager.UserManager.add_user"></a>
#### add\_user

```python
 | add_user(user: 'User') -> Union[User, Literal[False]]
```

Creates new user in the database

**Arguments**:

- `user` _User_ - User object
  

**Raises**:

- `NotImplementedError` - if authentication method is not implemented
  

**Returns**:

- `bool` - ``True`` on success, else False

<a name="riki_usermanager.UserManager.UserManager.get_user"></a>
#### get\_user

```python
 | get_user(username: str) -> Union['User', None]
```

Get `User` from the database

# Args:
- name (str): users name
# Returns:
- User | None: User object if user with the given username is found, otherwise nothing is returned.

<a name="riki_usermanager.UserManager.UserManager.delete_user"></a>
#### delete\_user

```python
 | delete_user(username: str) -> bool
```

Deletes user from the database

**Arguments**:

- `name` _str_ - users username
  

**Returns**:

- `bool` - True if delete was successful, otherwise False

<a name="riki_usermanager.UserManager.UserManager.update"></a>
#### update

```python
 | update(user: 'User') -> bool
```

Update user from userdata dictionary

**Arguments**:

- `name` _str_ - users username
- `userdata` _Dict[str, Any]_ - dictionary of user data
  

**Returns**:

- `bool` - True if delete was successful, otherwise False

<a name="riki_usermanager.UserManager.UserManager.check_password"></a>
#### check\_password

```python
 | @staticmethod
 | check_password(user: User, password: str) -> bool
```

Check if user password matches the password in the database

**Arguments**:

- `password` _str_ - user password
  

**Returns**:

- `bool` - did password match

