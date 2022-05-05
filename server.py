"""Server for INVESTABLE app."""
from flask import request, Flask, render_template, redirect, flash, session
import crud
from importlib_metadata import files
import os #to access os.environ to access secrets.sh values
# from jinja2 import StrictUndefined


app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')

#StrictUndefined is used to configure a Jinja2 setting that make it throw errors for undefined variables, helpful for debugging

# app.jinja_env.undefined = jinja2.StrictUndefined

@app.route('/')
def index():
    '''return homepage'''
    testing_session = session.get('price')
    session.modified = True
    return render_template('index.html')


@app.route('/calculator', methods=['POST'])
def to_calculate():
    '''return calculator interface'''
    
    price = request.form.get('price')
    down_payment = request.form.get('downpayment')
    rate = request.form.get('rate')
    mortgage = request.form.get('mortgage')
    closing = request.form.get('closing')
    rehab = request.form.get('rehab')
    rent = request.form.get('rent')
    taxes = request.form.get('taxes')
    insurance = request.form.get('insurance')
    hoa = request.form.get('hoa')
    utilities = request.form.get('utilities')
    maintenance = request.form.get('maintenance')
    pm = request.form.get('pm')
    vacancy = request.form.get('vacancy')
    capex = request.form.get('capex')
    
    flash('Running numbers')
    total_monthly_expenses = int(taxes) + int(insurance) + int(hoa) + int(utilities) + int(maintenance) + int(pm) + int(vacancy) + int(capex) + int(mortgage)
    cashflow = int(rent) - total_monthly_expenses
    
    #if user clicks SAVE, prompt LOGIN/SIGNUP and save data to db



    return render_template('calculator.html', cashflow=cashflow, price=price, downpayment=down_payment, rate=rate, closing=closing, rehab=rehab, rent=rent, taxes=taxes, insurance=insurance, hoa=hoa, utilities=utilities, maintenance=maintenance, pm=pm, vacancy=vacancy, capex=capex, mortgage=mortgage )


@app.route('/forum')
def to_read_post():
    '''if user is logged in, show dashboard features'''
    return render_template('forum.html')


@app.route('/news')
def get_news():
    '''show industry insight from news API'''
    return render_template('news.html')


@app.route('/books')
def get_books():
    '''show industry insight from goodreads API'''
    return render_template('books.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/register', methods=['GET'])
def register_user():
    '''Create a new user.'''

    email = request.form.get('email')
    password = request.form.get('password')

    # user = crud.get_user_by_email(email)
    # if user:
    #     flash('Cannot create an account with that email. Try again.')
    # else:
    #     user = crud.create_user(email, password)
    #     db.session.add(user)
    #     db.session.commit()
    #     flash('Account created! Please log in.')

    return render_template('register.html')


@app.route('/users/<user_id>')
def show_user(user_id):
    '''Show details on a particular user.'''

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)


@app.route('/login', methods=['GET'])
def process_login():
    '''Process user login.'''

    email = request.form.get('email')
    password = request.form.get('password')

    # user = crud.get_user_by_email(email)
    # if not user or user.password != password:
    #     flash('The email or password you entered was incorrect.')
    # else:
    #     # Log in user by storing the user's email in session
    #     session['user_email'] = user.email
    #     flash(f'Welcome back, {user.email}!')

    return render_template('login.html')
# sessions https://flask.palletsprojects.com/en/2.1.x/quickstart/#sessions
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         return do_the_login()
#     else:
#         return show_the_login_form()
# url_for('static', filename='style.css')
# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if valid_login(request.form['username'],
#                        request.form['password']):
#             return log_the_user_in(request.form['username'])
#         else:
#             error = 'Invalid username/password'
#     # the code below is executed if the request method
#     # was GET or the credentials were invalid
#     return render_template('login.html', error=error)
# https://flask.palletsprojects.com/en/2.1.x/patterns/fileuploads/ for uploading files
if __name__ == "__main__":
    # DebugToolbarExtension(app)

    app.run(debug=True)
