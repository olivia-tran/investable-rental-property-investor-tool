from flask import Flask, render_template
import os
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

################################


class Property(db.Model):


__tablename__ = 'properties'
id = db.Column


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


if __name__ == '__main__':
    app.run(debug=True)
