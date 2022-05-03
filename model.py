'''Models for INVESTABLE app'''
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    '''A user'''
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False, default='123456')
    imgURL = db.Column(db.String, default='#url')
    properties = db.relationship('Property', back_populates='user')
    blog_posts = db.relationship('BlogPost', back_populates='user')


    def __repr__(self):
        return f'<User: user_id= {self.user_id}, first_name= {self.first_name}>'

    @classmethod
    def create(cls, email, password):
        '''Create and return a new user.'''

        return cls(email=email, password=password)

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter(User.email == email).first()

    @classmethod
    def all_users(cls):
        return cls.query.all()


class Property(db.Model):
    '''A property data'''
    __tablename__ = 'properties'
    property_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    price = db.Column(db.Integer, nullable=False)
    interest_rate = db.Column(db.Integer, nullable=False)
    closing_costs = db.Column(db.Integer, nullable=False)
    rehab = db.Column(db.Integer)
    monthly_rent = db.Column(db.Integer, nullable=False)
    property_taxes = db.Column(db.Integer, nullable=False)
    insurance = db.Column(db.Integer, nullable=False)
    utilities = db.Column(db.Integer)
    misellaneous = db.Column(db.Integer)
    capex = db.Column(db.Integer)
    property_management = db.Column(db.Integer)
    vacancy = db.Column(db.Integer)
    address = db.Column(db.String)
    user = db.relationship('User', back_populates='properties') #one to many

    def __repr__(self):
        return f"<Property: property_id={self.property_id} user_id={self.user_id} at address={self.address}>"

    @classmethod
    def create(cls, user, property):
        '''Create and return a new property.'''

        return cls(user=user, property=property)


class BlogPost(db.Model):
    '''A blog post'''
    __tablename__ = 'blog_posts'
    blog_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    blog_content = db.Column(db.String, nullable=False)
    imgURL = db.Column(db.String)
    user = db.relationship('User', back_populates='blog_posts')

    def __repr__(self):
        return f"<Blog Post: blog_id={self.blog_id} user_id={self.user_id}>"


class Comment(db.Model):
    '''A blog comment'''
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog_posts.blog_id'))
    comment_content = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Comment: comment_id={self.comment_id} Blog Post={self.blog_id}, user_id={self.user_id}>"

class User_Images(db.Model):
    '''User Profile Picture '''
    image_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    imgURL = db.Column(db.String, default='static/')

class Blog_Images(db.Model):
    '''Blog Post Photos '''
    image_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

def connect_to_db(flask_app, db_uri='postgresql:///ratings', echo=True):  # what name should we use?
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
