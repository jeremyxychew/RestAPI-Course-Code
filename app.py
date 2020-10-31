import os

from flask import Flask
# reqparse - update variables that have been requested to change (PUT req)
from flask_restful import Api
from flask_jwt import JWT  # For authentication

# Import functions created in security.py
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
# IF 'DATABASE_URL' is not found in system, then sqlite:///data.db will be used as default db (e.g. when doing offline testing, online DB won't be available hence use sqlite DB)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///data.db')
# Turn off flask-SQLAlchemy modification tracker because SQLAlchemy main library has its own modification tracker (which is better)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# QUESTION: what is app.secret_key for ?
app.secret_key = 'jeremy'
api = Api(app)


# JWT - creates new endpoint /auth
# pass app = Flask(__name__), & functions authenticate and identity from security.py
jwt = JWT(app, authenticate, identity)


# Links app.py file to resources; resources will then link to model files
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')


# if line below: run app.run ONLY if we run app.py with python, and not because we are importing from other files
# importing a variable / class / method from another file runs the entire file. We may want to get certain variables but not want to run certain actions
# when executing a python file, python assigns name __main__ to that file
# that is why if statement below - only runs app.run if app.py is assigned name __main__
if __name__ == '__main__':
    # import db here to prevent circular import when other files (above) are looking to import db as well
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
