'''Models for INVESTABLE app'''
from collections import UserString
from datetime import datetime
from email.policy import default
from flask_sqlalchemy import SQLAlchemy
import pytz
db = SQLAlchemy()

# created_at
# order by id
# order by created at


class User(db.Model):
    '''A user'''
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False, default='123456')
    properties = db.relationship('Property', back_populates='user')
    blog_posts = db.relationship('BlogPost', back_populates='user')
    comments = db.relationship('Comment', back_populates='user')
    user_image = db.relationship(
        'UserImage', uselist=False, back_populates='user')

    def __repr__(self):
        return f'<User: id= {self.id}, first_name= {self.first_name}>'


class Property(db.Model):
    '''A property data'''
    __tablename__ = 'properties'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'))
    rent = db.Column(db.Float, nullable=False)
    mortgage = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, nullable=False)
    insurance = db.Column(db.Float, nullable=False)
    hoa = db.Column(db.Float)  
    utilities = db.Column(db.Float)
    maintenance = db.Column(db.Float)
    pm = db.Column(db.Float)
    vacancy = db.Column(db.Float)
    capex = db.Column(db.Float)
    user = db.relationship('User', back_populates='properties')  # one to many

    def __repr__(self):
        return f"<Property: id={self.id} user_id={self.user_id}>"




class BlogPost(db.Model):
    '''A blog post'''
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    blog_content = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(
        pytz.timezone('US/Pacific')), nullable=False)
    imgURL = db.Column(
        db.String, default='/static/aerialview.jpg', nullable=False)
    user = db.relationship('User', back_populates='blog_posts')
    comments = db.relationship('Comment', back_populates='blog_post')

    def __repr__(self):
        return f"<Blog Post: id={self.id} user_id={self.user_id}, created_at={self.created_at}>"


class Comment(db.Model):
    '''A blog comment'''
    __tablename__ = 'comments'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey(
        'blog_posts.id'), nullable=False)
    comment_content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(
        pytz.timezone('US/Pacific')), nullable=False)
    user = db.relationship('User', back_populates='comments')
    blog_post = db.relationship('BlogPost', back_populates='comments')

    def __repr__(self):
        return f"<Comment: comment_id={self.id} Blog Post={self.blog_id}, user_id={self.user_id}>, created_at={self.created_at}"


class UserImage(db.Model):
    '''User Profile Picture '''
    __tablename__ = 'user_images'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    imgURL = db.Column(db.String, default='static/default_photo.png')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', uselist=False, back_populates='user_image')


def example_data():
    '''Create example data for testing purposes'''
    user_1 = User(first_name='Baby', last_name='Yoda',
                  email='yoda@gmail.com', password=123456)
    user_2 = User(first_name='Luke', last_name='Skywalker',
                  email='luke@gmail.com', password=123456)
    db.session.add(user_1)
    db.session.add(user_2)
    db.session.commit()

    property_1 = Property(rent=1000, mortgage=500, tax=300, insurance=100)
    property_2 = Property(rent=1500, mortgage=400, tax=200, insurance=200)
    db.session.add(property_1)
    db.session.add(property_2)
    db.session.commit()


def connect_to_db(flask_app, db_uri='postgresql:///investables', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['UPLOAD_FOLDER'] = '/static/user_files'
    flask_app.config['MAX_CONTENT_LENGTH'] = 10 * \
        1024 * 1024  # 10 megabyte max upload

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the INVESTABLE db!')


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) for fewer query stmts
   

    connect_to_db(app)
