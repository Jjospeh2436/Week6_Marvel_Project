from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from marvel_shop.models import Customer, Comic, ComicOrder, Order, db, comic_schema, comics_schema

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/token', methods=['GET', 'POST'])
def token():
    data = request.json
    if data:
        client_id = data['client_id']
        access_token = create_access_token(identity = client_id)
        return {
            'status': 200,
            'access_token': access_token
        }
    else:
        return {
            'status': 400,
            'message': 'Missing Client Id. Try Again.'
        }
    
@api.route('/shop')
@jwt_required()
def get_shop():
    allcomics = Comic.query.all()
    response = comics_schema.dump(allcomics)
    return jsonify(response)

@api.route('/order/<cust_id>', methods = ['POST'])
@jwt_required()
def create_order(cust_id):

    data = request.json

    customer_order = data['order']

    customer = Customer.query.filter(Customer.cust_id == cust_id).first()
    if not customer:
        customer = Customer(cust_id)
        db.session(customer)
    
    order = Order()
    db.session.add(order)

    for comic in customer_order:

        comorder = ComicOrder(comic['com_id'], comic['quantity'], comic['price'], order.order_id, customer.cust_id)
        db.session.add(comorder)

        order.increment_ordertotal(comorder.price)

        current_comic = Comic.query.get(comic['com_id'])
        current_comic.decrement_quantity(comic['quanitty'])

    db.session.commit()

    return {
        'status': 200,
        'message' : 'New Order was Created.'
    }