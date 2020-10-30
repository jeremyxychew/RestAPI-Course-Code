# werkzeug: method to compare string (for older version of python)
from werkzeug.security import safe_str_cmp
# Import User class from user.py
from models.user import UserModel


# RETRIEVE AND STORE INTO SQL DB
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    # Retrieve user object with id mapping
    return UserModel.find_by_id(user_id)
