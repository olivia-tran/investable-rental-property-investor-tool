"""Server for catculator app."""
from flask import Flask, render_template

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


if __name__ == "__main__":
    # DebugToolbarExtension(app)

    app.run(debug=True)
