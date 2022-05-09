"""Server for INVESTABLE app."""
from flask import Flask, render_template, redirect, flash, session, request
import crud
import requests
import psycopg2

from model import connect_to_db, db, User
# from importlib_metadata import files
import os  # to access os.environ to access secrets.sh values
from jinja2 import StrictUndefined


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
    flash("welcome to the app")
    print(session)
    return render_template('index.html', GG_KEY=GG_KEY)


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
    total_monthly_expenses = int(taxes) + int(insurance) + int(hoa) + int(
        utilities) + int(maintenance) + int(pm) + int(vacancy) + int(capex) + int(mortgage)
    cashflow = int(rent) - total_monthly_expenses

    return render_template('calculator.html', cashflow=cashflow, price=price, downpayment=down_payment, rate=rate, closing=closing, rehab=rehab, rent=rent, taxes=taxes, insurance=insurance, hoa=hoa, utilities=utilities, maintenance=maintenance, pm=pm, vacancy=vacancy, capex=capex, mortgage=mortgage)


@app.route('/news')
def get_news():
    '''show industry insight from news API'''
    return redirect('/')


@app.route('/books')
def get_books():
    '''show industry insight from goodreads API'''
    return redirect('/')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
# ---------------------------Logged In Only Routes-------------------------------


@app.route('/register')
def register_page():
    '''landing page for register.'''
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_user():
    '''Create a new user.'''

    first = request.form.get('first')
    last = request.form.get('last')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email=email)
    if user:
        flash('Cannot create an account with that email. Try again.')
        return redirect('/register')
    else:
        user = crud.create_user(first, last, email, password)
        db.session.add(user)
        db.session.commit()
        flash('Account successfully created.')
        session['email'] = user.email

    return render_template('user_profile.html', first=first)


@app.route('/login')
def login_page():
    '''Landing page for user login.'''
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def process_login():
    '''Authenticate user login info.'''
    print(f'========================process login func')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email=email)
    if not user or user.password != password:
        flash('The email or password you entered was incorrect.')
        return redirect('/login')
    else:
        session['email'] = user.email
        flash(f'Welcome back, you\'re logging in using: {user.email}!')
        return redirect('/users')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/users')
def profile_page():
    return render_template('profile_page.html')


@app.route('/forum')
def to_read_post():
    '''if user is logged in, show dashboard features'''
    return render_template('forum.html')


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(debug=True)
