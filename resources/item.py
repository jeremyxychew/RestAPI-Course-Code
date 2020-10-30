from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    # Place parser in item class - so we don't have to redefine everywhere for where we use parser
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank."
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id."
                        )

    # Authentication required before we can run get method
    # Simply put @jwt_required() above functions that we want require token to use

    @jwt_required()
    def get(self, name):  # CRUD - 'READ'
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found in database.'}, 404

    def post(self, name):  # CRUD - 'CREATE'
        # if item is found in list i.e. if lambda function is not None
        if ItemModel.find_by_name(name):
            # 400 == bad request / something wrong with the request being made --> user fault
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
            # return a json payload from a request ; How we set Content-Type in Postman - if data is not json, will get an error

        # By this point, function would have checked that item to be added is NOT our db
        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        # except runs when unexpected error occur in inserting item in insert cls below
        except:
            # 500 -> internval server error (i.e. something went wrong, but can't point out exactly what went wrong) --> NOT user's fault, server's fault
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201  # Produce 201 status code (item has been CREATED)

    def delete(self, name):   # CRUD - 'DELETE'
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):   # CRUD - 'UPDATE'

        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        # since items are uniquely identified by id, can just simply save_to_db()
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        # return {'item': list(map(lambda x: x.json(), ItemModel.query.all()))}
