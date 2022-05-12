"""CRUD operations."""
from model import db, User, Property, BlogPost, Comment, BlogImage, UserImage, connect_to_db
import psycopg2
# Sign up


def create_user(first_name, last_name, email, password):
    '''Create and return a new user'''
    user = User(first_name=first_name, last_name=last_name,
                email=email, password=password)
    return user


def get_users():
    '''Return all users'''
    return User.query.all()


def get_user_by_id(user_id):
    '''Return a user by primary key'''
    return User.query.get(user_id)
# Log in: get user by email


def get_user_by_email(email):
    '''return a user by email'''
    return User.query.filter(User.email == email).first()


def create_property(user_id, mortgage, rent, tax, insurance, hoa, utilities, maintenance, capex, pm, vacancy):
    '''add to db and return a property'''
    new_property = Property(
        user_id=user_id,
        rent=rent,
        mortgage=mortgage,
        tax=tax,
        insurance=insurance,
        hoa=hoa,
        utilities=utilities,
        capex=capex,
        pm=pm,
        vacancy=vacancy,
        maintenance=maintenance

    )
    return new_property
# get a list of properties owned by one user via user_id


def get_properties_by_user(id):
    '''Return a list of properties owned by a user'''
    owned_properties = Property.query.filter(Property.user_id == id).all()
    return owned_properties
# when user logs in, we will have their email, from email get the id to query properties
# owned_properties is a list


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
