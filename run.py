from app import app
from db import db

db.init_app(app)


# run method directly before @app.before_first_request decorator before the first request is made
@app.before_first_request
def create_table():
    db.create_all()
