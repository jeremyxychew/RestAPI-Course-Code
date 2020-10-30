from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # This tells code that 'StoreModel' here has a relationship with 'ItemModel', goes into ItemModel and sees that item has variable 'store_id'
    # Below - this is a LIST of ItemModel ; can contain MORE THAN ONE item i.e. there can be many items to one store_id
    # lazy='dynamic' --> when we use this, self.items is no longer a list of items ; it is a query builder. With this, code will only go into items table when json(self) is called
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        # query.filter_by(name=name) essentially == SELECT * FROM items WHERE name=?
        # after that, pass query into ItemModel to create ItemModel object
        # .first() --> LIMIT 1 i.e. return only the first row of query
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        # don't need to tell sqlalchemy which row to insert vals into; we just need to tell sqlalchemy to insert object (i.e. 'self') into db
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
