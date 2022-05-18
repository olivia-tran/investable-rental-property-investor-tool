"""CRUD operations."""
from unicodedata import name
from model import db, User, Property, BlogPost, Comment, UserImage, connect_to_db
import psycopg2
from sqlalchemy import delete

#-----------------------------USER CRUD----------------------- 

def create_user(first_name, last_name, email, password):
    '''Create and return a new user'''
    user = User(first_name=first_name, last_name=last_name,
                email=email, password=password)
    return user


def get_users():
    '''Return all users'''
    return User.query.all()
def get_num_of_users():
    '''Get the total numbers of all active users'''
    user_nums = User.query.count()
  
    return user_nums

def get_user_by_id(user_id):
    '''Return a user by primary key'''
    return User.query.get(user_id)


def get_user_by_email(email):
    '''Return a user by email'''
    return User.query.filter(User.email == email).first()

def delete_user(email):
    '''Delete user data from db by email'''
    deleted_user = User.query.filter(User.email==email).first()
    db.session.delete(deleted_user)
    db.session.commit()
    # sometimes can return the deleted id back
#-----------------------------PROPERTY CRUD-----------------------  
    
def delete_property(id):
    '''Delete property from db by property Id'''
    deleted_property = Property.query.filter(Property.id==id).first()
    db.session.delete(deleted_property)
    db.session.commit()   


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
def get_num_of_properties():
    '''Get the total numbers of all properties saved by all users'''
    property_nums = Property.query.count()
    return property_nums 

def count_num_properties_by_a_user(user_id):
    '''Count the num of properties owned by a user'''
    count = Property.query.filter(Property.user_id==user_id).count()
    return count
    
def get_properties_by_user(id):
    '''Return a list of properties owned by a user'''
    owned_properties = Property.query.filter(Property.user_id == id).all()
    return owned_properties
# when user logs in, we will have their email, from email get the id to query properties
# owned_properties is a list
#-----------------------------BLOG CRUD-----------------------
def create_a_post(title, content, user_id, img_url=None):
     '''Create a blog post'''
     if img_url:
         blog = BlogPost(title=title, blog_content=content,user_id=user_id, imgURL=img_url)
     else:
         blog = BlogPost(title=title, blog_content=content,user_id=user_id)       

     return blog
 
def get_num_of_posts():
    '''Get the total numbers of posts created by all users'''
    post_nums = BlogPost.query.count()
  
    return post_nums 

def get_all_posts():
    '''Get all posts created by all users'''
    posts = BlogPost.query.all()
    return posts

def get_all_posts_by_a_user(user_id):
    '''Get all posts created by a user'''
    posts = BlogPost.query.filter(BlogPost.user_id==user_id).count()
    return posts

def get_blog_details(blog_id):
    '''Return blog details by blog ID'''
    post = BlogPost.query.get(blog_id)
    return post

#-----------------------------COMMENT CRUD-----------------------
def get_all_comments_by_a_user(user_id):
    '''Get all comments posted by a user'''
    comments = Comment.query.filter(Comment.user_id==user_id).count()
    return comments

def get_all_comments_on_a_post(blog_id):
    '''Get all comments replied to a post'''
    comments = Comment.query.filter(Comment.blog_id==blog_id).all()
    return comments
def get_num_of_comments():
    '''Get the total numbers of posts created by all users'''
    comments = Comment.query.count()
    return comments 
def create_a_comment(blog_id, user_id, comment_content):
    '''Create a comment on a blog post'''
    comment = Comment(blog_id=blog_id, user_id=user_id, comment_content=comment_content)
    return comment

def get_comment_details(comment_id):
    '''Return comment details by its ID'''
    comment = Comment.query.get(comment_id)
    return comment

#-----------------------------IMAGE CRUD----------------------- 
def save_profile_pic(url, user_id):
    '''Save profile pic to db'''
    profile_pic = UserImage(imgURL=url, user_id=user_id)
    return profile_pic

def get_img_url_by_email(email):
    '''Get the latest image url by email'''
    user_id = (get_user_by_email(email)).id
    img_url = (UserImage.query.filter_by(user_id=user_id).order_by(UserImage.id.desc()).first())
    if img_url != None:
        img_url= img_url.imgURL
        return img_url
    else:
        return 'static/pup.jpg'
        

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
