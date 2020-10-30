import sqlite3
from db import db


# UserModel here is an API
class UserModel(db.Model):
    __tablename__ = 'users'

    # Column 'id' of type 'Integer' and that it is the primary key (i.e. unique keys)
    id = db.Column(db.Integer, primary_key=True)
    # '80' - to limit the number of characters of username
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    # names above MUST match that in __init__ below i.e. self.id, self.username, self.password ; any other variables in it, not declared above, will not be saved in DB

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.random = 'Hello'  # This will not be saved in DB

    def save_to_db(self):
        db.session.add(self)  # Add 'self' object into db
        db.session.commit()

    # find_by_username and find_by_id are considered APIs; as long as we don't change these methods, codes elsewhere will not be affected
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
