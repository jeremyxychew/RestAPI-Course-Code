from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))  # 2 dp

    # Every ItemModel now has a property 'store' that is the store that matches 'store_id'
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # Below - variable 'store' here refers to a SINGLE store that the item is related / linked to
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

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
