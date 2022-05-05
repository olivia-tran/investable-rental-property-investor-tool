"""CRUD operations."""
from model import db, User, Property, BlogPost, Comment, BlogImage, UserImage, connect_to_db

def create_user(first_name, last_name, email, password):
    '''create and return a new user'''
    user = User(first_name=first_name, last_name=last_name, email=email, password=password)
    return user

def get_users():
    '''return all users'''
    return User.query.all()

def get_user_by_id(user_id):
    '''return a user by primary key'''
    return User.query.get(user_id)

def get_user_by_email(email):
    '''return a user by email'''
    return User.query.filter(User.email==email).first()

def add_property():
    '''add to db and return a property'''
    new_property = Property(
        price=price,
        down_payment=down_payment,
        interest_rate=interest_rate,
        mortgage = mortgage,
        closing_costs = closing_costs,
        rehab = rehab,
        monthly_rent = monthly_rent,
        property_taxes = property_taxes,
        insurance = insurance,
        hoa = hoa,
        utilities = utilities,
        misellaneous = misellaneous,
        capex = capex,
        property_management = property_management,
        vacancy = vacancy,
        address = address,
        city = city,
        state = state,
    )
    return property
if __name__ == "__main__":
    from server import app

    connect_to_db(app)