"""Server for INVESTABLE app."""
from flask import request, Flask, render_template, redirect, flash, session
from importlib_metadata import files
import os #to access os.environ to access secrets.sh values
import jinja2

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined

@app.route('/')
def index():
    '''return homepage'''
    testing_session = session.get('price')
    session.modified = True
    return render_template('index.html')
#why doesn't it save my cookies I have the secret key

@app.route('/calculator', methods=['POST'])
def to_calculate():
    '''return calculator interface'''
    
    price = request.form.get('price')
    down_payment = request.form.get('downpayment')
    rate = request.form.get('rate')
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
    total_monthly_expenses = int(taxes) + int(insurance) + int(hoa) + int(utilities) + int(maintenance) + int(pm) + int(vacancy) + int(capex)
    cashflow = int(rent) - total_monthly_expenses
    
    #if user clicks SAVE, prompt LOGIN/SIGNUP and save data to db



    return render_template('calculator.html', cashflow=cashflow, price=price, downpayment=down_payment, rate=rate, closing=closing, rehab=rehab, rent=rent, taxes=taxes, insurance=insurance, hoa=hoa, utilities=utilities, maintenance=maintenance, pm=pm, vacancy=vacancy, capex=capex )


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


@app.route('/thankyou')
def thank_you():
    return render_template('thankyou.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


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
