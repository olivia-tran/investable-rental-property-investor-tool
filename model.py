'''Models for INVESTABLE app'''
from collections import UserString
from datetime import datetime
# from email.policy import default
from flask_sqlalchemy import SQLAlchemy

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
    # blog_images = db.relationship('BlogImage', back_populates='user')
    comments = db.relationship('Comment', back_populates='user')
    user_image = db.relationship(
        'UserImage', uselist=False, back_populates='user')

    def __repr__(self):
        return f'<User: id= {self.id}, first_name= {self.first_name}>'

    # @classmethod
    # def create(cls, email, password):
    #     '''Create and return a new user.'''

    #     return cls(email=email, password=password)

    # @classmethod
    # def get_by_id(cls, id):
    #     return cls.query.get(id)

    # @classmethod
    # def get_by_email(cls, email):
    #     return cls.query.filter(User.email == email).first()

    # @classmethod
    # def all_users(cls):
    #     return cls.query.all()


class Property(db.Model):
    '''A property data'''
    __tablename__ = 'properties'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)
    rent = db.Column(db.Float, nullable=False)
    mortgage = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, nullable=False)
    insurance = db.Column(db.Float, nullable=False)
    hoa = db.Column(db.Float)  # need to update the data model
    utilities = db.Column(db.Float)
    maintenance = db.Column(db.Float)
    pm = db.Column(db.Float)
    vacancy = db.Column(db.Float)
    capex = db.Column(db.Float)

    user = db.relationship('User', back_populates='properties')  # one to many

    def __repr__(self):
        return f"<Property: id={self.id} user_id={self.user_id}>"

    # @classmethod
    # def create(cls, user, property):
    #     '''Create and return a new property.'''

    #     return cls(user=user, property=property)
#count of active users User.query.count()
#num of blog posts
#num of comments

class BlogPost(db.Model):
    '''A blog post'''
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    blog_content = db.Column(db.Text, nullable=False)
    # my blog_content is not nullable how did the post num 13 get committed?
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    imgURL = db.Column(db.String)
    title = db.Column(db.Text, nullable=False)
    user = db.relationship('User', back_populates='blog_posts')
    # blog_images = db.relationship('BlogImage', back_populates='blog_post')
    comments = db.relationship('Comment', back_populates='blog_post')

    def __repr__(self):
        return f"<Blog Post: id={self.id} user_id={self.user_id}, created_at={self.created_at}>"


class Comment(db.Model):
    '''A blog comment'''
    __tablename__ = 'comments'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'), nullable=False)
    comment_content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
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


# class BlogImage(db.Model):
#     '''Blog Post Photos '''
#     __tablename__ = 'blog_images'
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     imgURL = db.Column(db.String)
#     blog_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'), nullable=False)
#     blog_post = db.relationship('BlogPost', back_populates='blog_images')
#     user = db.relationship('User', back_populates='blog_images')


def connect_to_db(flask_app, db_uri='postgresql:///investables', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['UPLOAD_FOLDER'] = '/static/user_files'
    flask_app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 #10 megabyte max upload

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the INVESTABLE db!')


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
