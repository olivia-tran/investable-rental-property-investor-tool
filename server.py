"""Server for INVESTABLE app."""
from flask import Flask, render_template, redirect, flash, session, request, jsonify, json, url_for
import crud
import requests
import psycopg2
from model import connect_to_db, db, User
# from importlib_metadata import files
import os  # to access os.environ to access secrets.sh values
from jinja2 import StrictUndefined
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
GG_KEY = os.environ['GG_KEY']
API_KEY = os.environ['API_KEY']
# how to pass an object to from jinja to js?
# StrictUndefined is used to configure a Jinja2 setting that make it throw errors for undefined variables, helpful for debugging

app.jinja_env.undefined = StrictUndefined
# ---------------------------Not Logged In Routes-------------------------------


@app.route('/')
def index():
    '''Display homepage'''
    flash("Welcome to INVESTABLE community!")
    print(session)
    # print(f'counter===={session.get("counter", 0)}')
    return render_template('index.html', GG_KEY=GG_KEY)


@app.route('/calculator', methods=['POST'])
def to_calculate():
    '''Take user inputs to calculate rental cash flow'''

    print(len(request.form), " >>>>>>>>> form data: ", request.form)
    # print(len(request.json), " >>>>>>>>> form json: ", request.json)
    rent = request.form.get('rent', 0)
    mortgage = request.form.get('mortgage', 0)
    tax = request.form.get('tax', 0)
    insurance = request.form.get('insurance', 0)
    hoa = request.form.get('hoa', 0)
    utilities = request.form.get('utilities', 0)
    maintenance = request.form.get('maintenance', 0)
    pm = request.form.get('pm', 0)
    vacancy = request.form.get('vacancy', 0)
    capex = request.form.get('capex', 0)
    print(f'#######################{type(rent)}######################')
    flash('Running numbers')

    total_expenses = float(tax) + float(insurance) + float(hoa) + float(utilities) + float(
        maintenance) + float(pm) + float(vacancy) + float(capex) + float(mortgage)
    cashflow = float(rent) - total_expenses
    annual_cashflow = cashflow * 12
    print(f'===============cashflow = {cashflow}=====================')
#    return jsonify({'cashflow': cashflow, 'total_expenses': total_expenses,  'annual_cashflow': annual_cashflow})
    return redirect("/")
    # return render_template('calculator.html', cashflow=cashflow, rent=rent, tax=tax, insurance=insurance, hoa=hoa, utilities=utilities, maintenance=maintenance, pm=pm, vacancy=vacancy, capex=capex, mortgage=mortgage)



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

    return render_template('user_profile.html', first=first, last=last, GG_KEY=GG_KEY)
@app.route('/profile')
def user_profile():
    'Show user profile'
    if 'email' in session:
        email = session['email']
        user = crud.get_user_by_email(email)
        first = user.first_name
        last = user.last_name
        print(f'==========={user}')
        return render_template('user_profile.html', first=first, last=last, GG_KEY=GG_KEY)
    else:
        return redirect('/login')

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
    # test = jsonify({'owned_properties': owned_properties})
    # print(f'##############################{test}###########################')

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
    # how to get the id, it's from the button that user clicks on
    # how to check it here?
    crud.delete_property(id)
    flash(f'Property ID {id} was deleted.')
    return redirect('/properties')
# how to let user return to whichever page they were on previously prior to clicking delete


@ app.route('/forum')
@login_required
def forum():
    '''if user is logged in, show dashboard features'''
    return render_template('forum.html')


@ app.route('/contact')
@login_required
def contact_us():
    '''Allow user contact us to give feedback'''
    return render_template('contact_us.html')
# -------------------------------Handling image routes-------------------------------------
@app.route('/profile', methods=['POST'])
@login_required
def upload_profile_photo():
    '''Allow user upload profile picture'''
    profile_pic = request.files['profile_pic']
    if profile_pic.filename != '':
        profile_pic.save(profile_pic.filename)
    return redirect('/')
# -------------------------------Upload file routes-------------------------------------
# from werkzeug.utils import secure_filename

# @app.route('/upload')
# def upload_file():
#     '''Allow user upload files'''
#     return render_template('upload.html')

# @app.route('/uploader', methods = ['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         f = request.files['file']
#         f.save(secure_filename(f.filename))
#         return 'File uploaded successfully'


# -------------------------------JSON routes-------------------------------------


# @ app.route('/properties.json')
# def show_properties_owned_by_user():
#     email = session['email']
#     user = crud.get_user_by_email(email)
#     id = user.id
#     print(f'=====================email={email}=================')
#     owned_properties = crud.get_properties_by_user(id)
#     print(
#         f'====================owned_properties={owned_properties}=================')
#     print(f'TYPE====================={type(owned_properties)}==========')

    # return jsonify({'rent': owned_properties.rent,
    #                 'id': owned_properties.id,
    #                 'mortgage': owned_properties.mortgage,
    #                 'tax': owned_properties.tax,
    #                 'insurance': owned_properties.insurance,
    #                 'hoa': owned_properties.hoa
    #                 })


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(debug=True)
# host='0.0.0.0', port=8080
