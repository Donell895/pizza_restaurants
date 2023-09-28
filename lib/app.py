
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Restaurant, RestaurantPizza, Pizza


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza_restaurants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    restaurant_list = []
    
    for restaurant in restaurants:
        restaurant_data = {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address
        }
        restaurant_list.append(restaurant_data)
    
    return jsonify(restaurant_list)


@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)

    if restaurant:
        restaurant_data = {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            
        }
        return jsonify(restaurant_data)
    else:
        return jsonify({'error': 'Restaurant not found'}), 404


@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)

    if restaurant:
        try:
            
            RestaurantPizza.query.filter_by(restaurant_id=id).delete()
            db.session.delete(restaurant)
            db.session.commit()
            return '', 204
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'IntegrityError occurred while deleting the restaurant'}), 500
    else:
        return jsonify({'error': 'Restaurant not found'}), 404


@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    pizza_list = []
    
    for pizza in pizzas:
        pizza_data = {
            'id': pizza.id,
            'name': pizza.name,
            'ingredients': pizza.ingredients
        }
        pizza_list.append(pizza_data)
    
    return jsonify(pizza_list)


@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()

    if not data or 'price' not in data or 'pizza_id' not in data or 'restaurant_id' not in data:
        return jsonify({'errors': ['Missing required fields']}), 400

    try:
        price = float(data['price'])
    except ValueError:
        return jsonify({'errors': ['Invalid price format']}), 400

    restaurant = Restaurant.query.get(data['restaurant_id'])
    pizza = Pizza.query.get(data['pizza_id'])

    if not restaurant or not pizza:
        return jsonify({'errors': ['Invalid restaurant or pizza']}), 400

    restaurant_pizza = RestaurantPizza(price=price, restaurant=restaurant, pizza=pizza)

    db.session.add(restaurant_pizza)
    db.session.commit()

    pizza_data = {
        'id': pizza.id,
        'name': pizza.name,
        'ingredients': pizza.ingredients
    }

    return jsonify(pizza_data), 201

if __name__ == '__main__':
    app.run(port=5555)