"""Server for INVESTABLE app."""
from datetime import datetime
from flask import Flask, render_template, redirect, flash, session, request, jsonify, json, url_for, make_response
import crud
import cloudinary.uploader
import requests
import psycopg2
import os
import random
import pytz
import pandas as pd
from model import connect_to_db, db, User

from jinja2 import StrictUndefined
from functools import wraps
from data import QUOTES

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
GG_KEY = os.environ['GG_KEY']
API_KEY = os.environ['API_KEY']
CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUD_NAME = 'investable'
# FRED_KEY = os.environ['FRED_KEY'] https://fred.stlouisfed.org/ Economic Research Federal Reserve Data API


# StrictUndefined is used to configure a Jinja2 setting that make it throw errors for undefined variables, helpful for debugging

app.jinja_env.undefined = StrictUndefined
# ---------------------------Not Logged In Routes-------------------------------


@app.route('/')
def index():
    '''Display homepage'''
    # flash("Welcome to INVESTABLE community!")
    print(session)
    return render_template('index.html', GG_KEY=GG_KEY, API_KEY=API_KEY)


@ app.route('/books')
def get_books():
    '''Show related to rental property investment books from Google Books API'''
    return redirect('/')
 # non-authenticated users have access to book recommendation implemented by Google Books API


@ app.route('/news')
def get_news():
    '''Show industry insight from News API'''
    return redirect('/')
 # non-authenticated users have access to industry news by News API which offer articles published from 80,000 sources


@ app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
# ---------------------------Logged In Only Routes-------------------------------


@ app.route('/register')
def register_page():
    '''Landing page for register.'''
    return render_template('register.html', GG_KEY=GG_KEY)


@ app.route('/register', methods=['GET', 'POST'])
def register_user():
    '''Create a new user.'''
    if request.method == 'GET':
        flash('if stmt request.method == get')
        return render_template('properties.html', GG_KEY=GG_KEY)
    else:
        email = request.form.get('email')
        if crud.get_user_by_email(email):
            flash('Cannot create an account with that email🤔. Try again.', 'error')
            return redirect('/register')
        else:
            first = request.form.get('first')
            last = request.form.get('last')
            email = request.form.get('email')
            password = request.form.get('password')
            user = crud.create_user(first, last, email, password)
            db.session.add(user)
            db.session.commit()
            flash('Account was successfully created. 🥳️', 'info')
            session['email'] = user.email
            user_id = (crud.get_user_by_email(email)).id
            properties = crud.get_properties_by_user(user_id)
    return render_template('properties.html', user=user, properties=properties, GG_KEY=GG_KEY, session=session)
# I started using the app as if a user testing here and have updated a few formatting filters to increase user's expererience.E:g. titlecase for names
# I really like having those print stmts which make it easier for debugging, so I'll just comment them out when deployed


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        '''To set up @login_required decorator'''
        if 'email' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function


@ app.route('/login')
def login_page():
    '''Landing page for user login.'''
    return render_template('login.html')


@ app.route('/login', methods=['POST'])
def process_login():
    '''Authenticate user login info.'''

    email = request.form.get('email')
    password = request.form.get('password')

    print(
        f'========================process login func request.form={request.form}')
    user = crud.get_user_by_email(email=email)
    if not user or user.password != password:
        flash('The email or password you entered was incorrect 🤔. Try again', 'error')
        return redirect('/login')
    else:
        session['email'] = user.email
        # get user by email and then store id in session
        user = crud.get_user_by_email(email)
        id = user.id
        # print(f'user in login func = {user}====================')
        # print(f'user ID in login func = {id}====================')
        flash(f'😺Welcome back, you\'re logging in using: {user.email}!')
        return redirect('/properties')


@app.route('/profile')
def user_profile():
    'Show user profile'
    if 'email' in session:
        email = session['email']
        user = crud.get_user_by_email(email)
        count = crud.get_all_posts_by_a_user(user.id)
        property_count = crud.count_num_properties_by_a_user(user.id)
        show_posts = crud.show_posts_by_a_user_desc(user.id)
        img_url = crud.get_img_url_by_email(email)
        count = crud.get_all_posts_by_a_user(user.id)
        comment_count = crud.get_all_comments_by_a_user(user.id)
        print(f'==========={user}')
        return render_template('user_profile.html', comment_count=comment_count, user=user, count=count, property_count=property_count, show_posts=show_posts, img_url=img_url, GG_KEY=GG_KEY, API_KEY=API_KEY, session=session)
    else:
        return redirect('/login')


@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def update_profile(user_id):
    '''Update user profile name, email or password'''
    user = crud.get_user_by_email(session['email'])
    if request.method == 'POST':
        if user and user.password == request.form.get('old-password'):
            user.first_name = request.form.get('first')
            user.last_name = request.form.get('last')
            # user.email = request.form.get('email')
            user.password = request.form.get('password')
            db.session.add(user)
            db.session.commit()
            flash('Account was succesfully updated! ')
        else:
            flash(
                f'User {user_id} was not found or old password was enterred incorrectly. ')
        return redirect('/profile')
    else:
        return render_template('update_user_info.html', user=user)


@app.route('/profile/<int:user_id>/delete', methods=['POST'])
@login_required
def to_delete_account(user_id):
    '''Delete user account by user ID'''
    # check user_id to be deleted vs current_user.id
    # to keep vs to delete all posts done by deleted users, I decided to keep all related posts/comments by deleted users. Cascades

    user = crud.get_user_by_email(session['email'])
    if user_id == user.id:
        crud.delete_user(user_id)
        flash(f'Your account was deactivated.')
        session.clear()
        return redirect('/contact')
    else:
        flash('Sorry, can\'t delete that user!')


@ app.route('/logout')
def logout():
    session.clear()
    flash('You were logged out.')
    return redirect('/')


@ app.route('/properties')
@login_required
def property_page():
    email = session['email']
    user = crud.get_user_by_email(email)
    properties = crud.get_properties_by_user(user.id)
    print(f'====================={properties}=================')
    return render_template('properties.html', properties=properties, user=user)


@ app.route('/save_data', methods=['GET', 'POST'])
@login_required
def save_data():
    '''Save property data to db.'''
    rent = request.form.get('rent')
    mortgage = request.form.get('mortgage')
    maintenance = request.form.get('maintenance')
    tax = request.form.get('tax')
    insurance = request.form.get('insurance')
    hoa = request.form.get('hoa')
    utilities = request.form.get('utilities')
    capex = request.form.get('capex')
    pm = request.form.get('pm')
    vacancy = request.form.get('vacancy')
    email = session['email']
    user = crud.get_user_by_email(email)
    user_id = user.id
    new_property = crud.create_property(
        user_id, mortgage, rent, tax, insurance, hoa, utilities, maintenance, capex, pm, vacancy)
    db.session.add(new_property)
    db.session.commit()

    flash('Property was successfully saved! 🥳️')
    return redirect('/properties')


@app.route('/properties/<int:id>/delete', methods=['POST'])
@login_required
def to_delete_property(id):
    '''Delete a property by ID'''
    crud.delete_property(id)
    flash(f'Property ID {id} was deleted.')
    return redirect('/properties')


@ app.route('/contact', methods=['GET', 'POST'])
def contact():
    '''Allow user contact us to give feedback'''
    if request.method == 'POST':
        email = request.form.get('email')
        feedback = request.form.get('textarea')
        data = pd.DataFrame({'email': email, 'feedback': feedback}, index=[0])
        with open('data/userFeedback.csv', 'a') as f:
            data.to_csv(f)
        flash('Thank you for your message!')
    return render_template('contact.html')
    # this saves but not overwriting old content in the csv file


# -------------------------------Related to BLOG POSTS routes-------------------------------------


@ app.route('/forum')
@login_required
def forum():
    '''if user is logged in, show dashboard features'''
    total_comments = crud.get_num_of_comments()
    total_posts = crud.get_num_of_posts()
    total_users = crud.get_num_of_users()
    total_properties = crud.get_num_of_properties()
    posts = crud.show_posts_by_order()
    return render_template('forum.html', total_comments=total_comments, posts=posts, user_nums=total_users, post_nums=total_posts, property_nums=total_properties)


@ app.route('/blogging', methods=['GET', 'POST'])
@login_required
def blogging():
    '''if user is logged in, user can create blog posts'''
    if request.method == 'GET':
        return render_template('posting.html')
    else:

        user_id = get_user_by_session_email().id
        blog_content = request.form.get('blog_content')
        print(f' this is BLOG CONTENT====={blog_content}')
        title = request.form.get('title')
        # test = request.form.get('test')
        # print(f' this is BLOG TESTTTTTTTT====={test}')
        print(f' this is BLOG TITLE====={title}')
        blog_photo = request.files.get('blog_image')
        print(f' this is BLOG PHOTO====={blog_photo}')
        # if user chooses to add a photo in the post
        if blog_photo:
            print(f'==================={request.files}')
            img_url = upload_to_cloudinary(blog_photo)
            blog = crud.create_a_post(user_id, blog_content, title, img_url)
            # flash('IF STMT RAN')
        else:
            blog = crud.create_a_post(user_id, blog_content, title)
            # flash('ELSE STMT RAN')
        db.session.add(blog)
        db.session.commit()
        flash('Blog was created!')
        return redirect('/forum')


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    '''Accept searched keyword by user, output searched results'''
    if request.method == 'POST':
        searched_keyword = request.form.get('searched_keyword')
        searched_posts = crud.search_blog_posts(searched_keyword)
        print(f'THIS IS searched_result= {searched_posts}')
        return render_template('search.html', searched_posts=searched_posts, searched_keyword=searched_keyword)
    else:
        return redirect('/forum')
    # prefer routing user back to search page if hit refresh


@app.route('/forum/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def to_delete_post(id):
    '''Delete a post by ID'''
    user = crud.get_user_by_email(session['email'])
    print(f"$$$$$$$$$$$$$$$$$$$$$${user.blog_posts}")
    if user.blog_posts[0].id == id:
        print(
            f'$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$user.blog_posts[0].id{user.blog_posts[0].id}')
        crud.delete_post(id)
        flash(f'Blog Post ID {id} was deleted.')
    else:
        flash('Can\'t delete the post. Please check if you\'re the author')
    return redirect('/forum')


@app.route('/forum/<int:blog_id>/update', methods=['GET', 'POST'])
@login_required
def to_update_post(blog_id):
    '''Update a post by its ID'''
    # current user
    user = crud.get_user_by_email(session['email'])
    # blog id being passed in
    post = crud.get_blog_details(blog_id)
    # check if current author is the same as user_id
    if request.method == 'POST':
        if user.id == post.user_id:
            # flash('Outer if ran')
            post.title = request.form.get('title')
            post.blog_content = request.form.get('blog_content')
            blog_photo = request.files.get('blog_image')
            if blog_photo:
                # flash('Inner if ran')
                post.imgURL = upload_to_cloudinary(blog_photo)
            db.session.add(post)
            db.session.commit()
            flash('Blog was updated!')
        else:
            flash(f'No blog post ID {blog_id} was found.')
        return redirect(f'/forum/{blog_id}')
    else:
        return render_template('update.html', post=post)


# ------------------------------COMMENT routes----------------


@app.route('/forum/<int:blog_id>', methods=['GET', 'POST'])
@login_required
def to_post_a_comment(blog_id):
    '''To leave a comment on a blog post'''
    if request.method == 'GET':
        # flash('IF STMT ')
        user_id = get_user_by_session_email().id
        post = crud.get_blog_details(blog_id)
        comments = crud.get_all_comments_on_a_post(blog_id)
        return render_template('blog_details.html', datetime=datetime, pytz=pytz, comments=comments, post=post, user_id=user_id)
    else:
        # flash('ELSE STMT')
        # flash('The comment is to be posted.')
        comment_content = request.form.get('comment-content')
        # to make sure users type a comment that is longer than 10 characters
        if len(comment_content) > 10:
            user_id = get_user_by_session_email().id
            comment = crud.create_a_comment(blog_id, user_id, comment_content)
            db.session.add(comment)
            db.session.commit()
            flash(f'Comment was successfully posted.')
        else:
            flash('Please write a longer response')
        return redirect(f'/forum/{blog_id}')


# -------------------------------Handling User IMAGES routes-------------------------------------
@app.route('/post-form-data', methods=['POST'])
@login_required
def upload_profile_photo():
    '''Process form data and redirect to /show_profile_image page'''
    my_file = request.files['my-file']
    img_url = upload_to_cloudinary(my_file)
    add_user_img_record(img_url)
    flash('Your picture has been successfully uploaded!')
    return redirect('/profile')


@app.route('/profile_image')
@login_required
def show_profile_image():
    '''Show the profile pic uploaded by user'''
    email = session['email']
    user = crud.get_user_by_email(email)
    user_id = (crud.get_user_by_email(email)).id
    posts = crud.get_all_posts_by_a_user(user_id)
    property_count = crud.count_num_properties_by_a_user(user_id)
    count = crud.get_all_posts_by_a_user(user_id)
    img_url = crud.get_img_url_by_email(email)
    return render_template('user_profile.html', img_url=img_url, GG_KEY=GG_KEY, count=count, posts=posts, property_count=property_count, user=user)


# -------------------------------HELPER functions-------------------------------------
def upload_to_cloudinary(media_file):
    '''Upload media file to cloudinary'''
    result = cloudinary.uploader.upload(
        media_file, api_key=CLOUDINARY_KEY, api_secret=CLOUDINARY_SECRET, cloud_name=CLOUD_NAME)
    return result['secure_url']


def add_user_img_record(img_url):
    '''Save img url to db by user ID'''
    print('\n'.join(
        [f"{'*' * 20}", 'Save this url to your database!', img_url, f"{'*' * 20}"]))
    user = get_user_by_session_email()
    print(f'user_id==============={user.id}')
    new_pic = crud.save_profile_pic(url=img_url, user_id=user.id)
    db.session.add(new_pic)
    db.session.commit()
    # flash('Image URL saved to db!')

# to remove this and refactor code


def get_user_by_session_email():
    '''get a user via accessing session['email']'''
    email = session.get('email')
    user = crud.get_user_by_email(email)
    return user

# pass variables to base.html


@app.context_processor
def base():
    '''Pass variables to base.html'''
    user = get_user_by_session_email()
    return dict(user=user)

# -----------------------------API Routes---------------------------


@app.route('/quotes.json')
def get_quotes():
    '''send jsonified quotes to front end'''
    return jsonify({"quotes": QUOTES})


@app.route('/compare-properties.json', methods=['POST'])
def send_property_data_to_charts():
    '''Use property ID from JS to query db and send corresponding data back to JS for charts'''

    property_ids = request.json.get('propertyIds')

    print("  (((((((((()))))))))))) what is the id: ", property_ids)
    print(f'PROPERTY_ID received from JS=== {type(property_ids)}')

    properties_data = []
    for property_id in property_ids:
        property_data = crud.get_property_details_by_id(property_id)
        properties_data.append(property_data.__dict__)
        print(f'PROPERTY DATA FROM DB===={property_data}')
        print(f'PROPERTIESSSSS DATA FROM DB===={type(properties_data)}')
        properties_data[-1].pop('_sa_instance_state')
    print(f'PROPERTIESSSSS DATA FROM DB===={properties_data}')

    return jsonify(properties_data)


# -------------------------------JSON routes-------------------------------------


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run()
    # app.run(debug=True)
# host='0.0.0.0', port=8080
