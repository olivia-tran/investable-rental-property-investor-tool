"""Server for catculator app."""
from flask import request
from flask import Flask, render_template
from importlib_metadata import files

app = Flask(__name__)


# Replace this with routes and view functions!
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculator')
def to_calculate():
    return render_template('index.html')


@app.route('/forum')
def to_read_post():
    return render_template('forum.html')


@app.route('/news')
def get_news():
    return render_template('news.html')


@app.route('/books')
def get_books():
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
