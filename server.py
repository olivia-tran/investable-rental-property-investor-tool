"""Server for INVESTABLE app."""
from flask import Flask, render_template, redirect, flash, session, request, jsonify, json, url_for
import crud, requests, psycopg2, os, cloudinary.uploader, random
from model import connect_to_db, db, User
# from importlib_metadata import files
from jinja2 import StrictUndefined
from functools import wraps
from real_estate_quotes import QUOTES

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
GG_KEY = os.environ['GG_KEY']
API_KEY = os.environ['API_KEY']
CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUD_NAME = 'investable'
FRED_KEY = os.environ['FRED_KEY']
# how to pass an object to from jinja to js?
# StrictUndefined is used to configure a Jinja2 setting that make it throw errors for undefined variables, helpful for debugging

app.jinja_env.undefined = StrictUndefined
# ---------------------------Not Logged In Routes-------------------------------


@app.route('/')
def index():
    '''Display homepage'''
    # flash("Welcome to INVESTABLE community!")
    print(session)
    # print(f'counter===={session.get("counter", 0)}')
    return render_template('index.html', GG_KEY=GG_KEY)


# @app.route('/save_data')
# def to_make_charts():
#     '''Take user inputs to send a json object to chart js'''
#     print(len(request.form), " >>>>>>>>> form data: ", request.form)
#     rent=request.form.get('rent')
#     mortgage=request.form.get('mortgage')
#     print(f'mortgage={mortgage}')
#     maintenance=request.form.get('maintenance')
#     tax=request.form.get('tax')
#     insurance=request.form.get('insurance')
#     hoa=request.form.get('hoa')
#     utilities=request.form.get('utilities')
#     capex=request.form.get('capex')
#     pm=request.form.get('pm')
#     vacancy=request.form.get('vacancy')
    # return jsonify({'Rent': rent, 
    #                 'Mortgage': mortgage, 
    #                 'Tax': tax,
    #                 'Insurance': insurance,
    #                 'HOA': hoa, 
    #                 'Utilities': utilities,
    #                 'Maintenance': maintenance,
    #                 'PM': pm, 
    #                 'Vacancy': vacancy,
    #                 'CapEx': capex
        
    # })
   



@ app.route('/books')
def get_books():
    '''Show related to rental property investment books from Books API'''
    return redirect('/')


@ app.route('/news')
def get_news():
    '''Show industry insight from News API'''
    return redirect('/')


@ app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
# ---------------------------Logged In Only Routes-------------------------------


@ app.route('/register')
def register_page():
    '''Landing page for register.'''
    return render_template('register.html', GG_KEY=GG_KEY)


@ app.route('/register', methods=['POST'])
def register_user():
    '''Create a new user.'''

    first = request.form.get('first')
    last = request.form.get('last')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email=email)
    if user:
        flash('Cannot create an account with that email🤔. Try again.', 'error')
        return redirect('/register')
    else:
        user = crud.create_user(first, last, email, password)
        db.session.add(user)
        db.session.commit()
        flash('Account successfully created. 🥳️', 'info')
        session['email'] = user.email

    return render_template('user_profile.html', user=user, GG_KEY=GG_KEY)


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
    
    print(f'========================process login func request.form={request.form}')
    user = crud.get_user_by_email(email=email)
    if not user or user.password != password:
        flash('The email or password you entered was incorrect 🤔. Try again', 'error')
        return redirect('/login')
    else:
        session['email'] = user.email
        # get user by email and then store id in session
        user = crud.get_user_by_email(email)
        id = user.id
        print(f'user in login func = {user}====================')
        print(f'user ID in login func = {id}====================')
        flash(f'😺Welcome back, you\'re logging in using: {user.email}!')
        return redirect('/properties')
    
@app.route('/profile')
def user_profile():
    'Show user profile'
    if 'email' in session:
        email = session['email']
        user = crud.get_user_by_email(email)
        first = user.first_name
        last = user.last_name
        user_id = user.id
        posts = crud.get_all_posts_by_a_user(user_id)
        property_count = crud.count_num_properties_by_a_user(user_id)
        img_url = crud.get_img_url_by_email(email)
        print(f'==========={user}')
        return render_template('user_profile.html', user=user, posts=posts, property_count=property_count, img_url=img_url, GG_KEY=GG_KEY)
    else:
        return redirect('/login')

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
    id = user.id
    print(f'=====================email={email}=================')
    properties = crud.get_properties_by_user(id)
    print(f'====================={properties}=================')
    return render_template('properties.html', properties=properties, user=user)

@ app.route('/save_data', methods=['GET','POST'])
@login_required
def save_data():
    '''Save property data to db.'''
    rent=request.form.get('rent')
    mortgage=request.form.get('mortgage')
    maintenance=request.form.get('maintenance')
    tax=request.form.get('tax')
    insurance=request.form.get('insurance')
    hoa=request.form.get('hoa')
    utilities=request.form.get('utilities')
    capex=request.form.get('capex')
    pm=request.form.get('pm')
    vacancy=request.form.get('vacancy')
    email = session['email']
    user = crud.get_user_by_email(email)
    user_id = user.id
    new_property = crud.create_property(user_id, mortgage, rent, tax, insurance, hoa, utilities, maintenance, capex, pm, vacancy)
    db.session.add(new_property)
    db.session.commit()
    
    flash('Property was successfully saved! 🥳️')
    return redirect('/properties')

@app.route('/properties/<int:id>/delete', methods=['POST'])
@login_required
def to_delete_property(id):
    '''Delete a property by ID'''
    # flash('The property is about to be deleted.')
    crud.delete_property(id)
    flash(f'Property ID {id} was deleted.')
    return redirect('/properties')
# how to let user return to whichever page they were on previously prior to clicking delete

@ app.route('/contact')
@login_required
def contact_us():
    '''Allow user contact us to give feedback'''
    return render_template('contact_us.html')

# -------------------------------Related to blogging routes-------------------------------------
@ app.route('/forum')
@login_required
def forum():
    '''if user is logged in, show dashboard features'''
    # total_comments = crud.get_num_of_comments()
    total_posts = crud.get_num_of_posts()
    total_users = crud.get_num_of_users()
    total_properties = crud.get_num_of_properties()
    posts = crud.get_all_posts()
    for post in posts:
        full_name = crud.get_user_full_name(post.user_id)
    return render_template('forum.html', full_name=full_name, posts=posts, user_nums=total_users, post_nums=total_posts, property_nums= total_properties)

@ app.route('/blogging', methods=['POST'])
@login_required
def blogging():
    '''if user is logged in, user can create blog posts'''
    print('=====THIS IS BLOGGING FUNCTION=====')
    title = request.form.get('title')
    print('=====THIS IS BLOGGING FUNCTION=====')
    blog_content = request.form.get('blog-content')
    email = session['email']
    user = crud.get_user_by_email(email)
    user_id = user.id
    blog = crud.create_a_post(title, blog_content, user_id)
    db.session.add(blog)
    db.session.commit()
    flash('Blog was created!')
    return redirect('/forum')
    # return render_template('posting.html')
    
@app.route('/create_a_post')
@login_required
def create_a_post():
    '''Create a post using normal routing'''
    return render_template('posting.html')

@app.route('/forum/<int:id>', methods=['POST'])
@login_required
def read_post(id):
    '''Read details of a blog post'''
    post = crud.get_blog_details(id)
    return render_template('blog_details.html', post=post )
# page doesn't display my navbar correctly

# -------------------------------Handling image routes-------------------------------------
@app.route('/post-form-data', methods=['POST'])
@login_required
def upload_profile_photo():
    '''Process form data and redirect to /show_profile_image page'''
    my_file = request.files['my-file']
    img_url = upload_to_cloudinary(my_file)
    add_user_img_record(img_url)
    flash('Your picture has been successfully uploaded!')
    return redirect(url_for('show_profile_image', img_url=img_url))
   
@app.route('/profile_image')
@login_required
def show_profile_image():
    '''Show the profile pic uploaded by user'''
    email=session['email']
    user = crud.get_user_by_email(email)
    user_id = (crud.get_user_by_email(email)).id
    posts = crud.get_all_posts_by_a_user(user_id)
    property_count = crud.count_num_properties_by_a_user(user_id)
    # img_url = request.args.get('img_url')
    img_url = crud.get_img_url_by_email(email)
    return render_template('user_profile.html', img_url=img_url, GG_KEY=GG_KEY, posts=posts, property_count=property_count, user=user)
# this shows the pic on the diff page which is not what I want 
   



# -------------------------------Upload file routes-------------------------------------
def upload_to_cloudinary(media_file):
    '''Upload media file to cloudinary'''
    result = cloudinary.uploader.upload(media_file, api_key=CLOUDINARY_KEY, api_secret=CLOUDINARY_SECRET, cloud_name=CLOUD_NAME)
    return result['secure_url']

def add_user_img_record(img_url):
    '''Save img url to db by user ID'''
    print('\n'.join([f"{'*' * 20}", 'Save this url to your database!', img_url, f"{'*' * 20}"]))
    user_id = (crud.get_user_by_email(session['email'])).id
    print(f'user_id==============={user_id}')
    new_pic = crud.save_profile_pic(url=img_url, user_id=user_id)
    db.session.add(new_pic)
    db.session.commit()
    flash('Image URL saved to db!')

#-----------------------------API Routes---------------------------
@app.route('/quotes.json')
def get_quotes():
    '''send jsonified quotes to front end'''
    return jsonify({"quotes": QUOTES})

        



# -------------------------------JSON routes-------------------------------------




if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(debug=True)
# host='0.0.0.0', port=8080
