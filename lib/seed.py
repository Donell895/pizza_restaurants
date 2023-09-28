from models import Restaurant, Pizza, RestaurantPizza, db
from faker import Faker
from app import app

import random


fake = Faker()

def seed_database():
    with app.app_context():

    
        for _ in range(5):
            restaurant = Restaurant(
                name=fake.company(),
                address=fake.address(),
            )
            db.session.add(restaurant)

        # Create and seed pizza types
        pizzas_data = [
            {"name": "Cheese", "ingredients": "Dough, Tomato Sauce, Cheese"},
            {"name": "Pepperoni", "ingredients": "Dough, Tomato Sauce, Cheese, Pepperoni"},
            {"name": "Margherita", "ingredients": "Dough, Tomato Sauce, Cheese, Basil"},
            {"name": "Vegetarian", "ingredients": "Dough, Tomato Sauce, Cheese, Various Vegetables"},
            {"name": "Hawaiian", "ingredients": "Dough, Tomato Sauce, Cheese, Ham, Pineapple"},
        ]

        for pizza_data in pizzas_data:
            pizza = Pizza(**pizza_data)
            db.session.add(pizza)

        
        db.session.commit()

        
        restaurants = Restaurant.query.all()
        pizzas = Pizza.query.all()

        
        for _ in range(10):
            random_price = round(random.uniform(5, 30), 2)
            restaurant = random.choice(restaurants)
            pizza = random.choice(pizzas)

            restaurant_pizza = RestaurantPizza(
                price=random_price,
                restaurant=restaurant,
                pizza=pizza,
            )
            db.session.add(restaurant_pizza)

        
        db.session.commit()

if __name__ == '__main__':
    seed_database()