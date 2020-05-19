from flask import session, render_template, request, redirect, url_for
from project1.models import Book, User, Review
from project1 import app
import csv

from project1 import db

# Route to the main homepage
@app.route("/")
def index():
    """Default page"""

    return redirect(url_for('login')) # Start by going directly to login page

@app.route("/login", methods=['GET', 'POST'])
def login():
    """Login page"""

    if request.method == 'POST':
        name = request.form.get("username")
        password = request.form.get("password")
        return f"{name} : {password}"
    else:
        return render_template('login.html', title="Login Page", heading="Login")

@app.route("/register")
def register():
    """Used to register a new user"""

@app.route("/UserProfile/<string:username>")
def profile(username):
    """Loads the books and reviews of a specific user
    given the users username"""

@app.route("/book/<int:id>")
def book(id):
    """Displays a specific book and its information
    given that books id."""


def main():
    """This method is used to load all of the book data
    initially from the data file."""

    # Load all of the data into the database
    f = open("project1/books.csv")
    reader = csv.reader(f)

    # Cycle through the rest of the file and load data into DB
    for id, title, author, year in reader:
        #print(f"{id},  {title},  {author},  {year}")
        book = Book(isbn=id, title=title, author=author, year=year, count_ratings=0, overall_rating=0)
        db.session.add(book)

    #Commit Changes
    db.session.commit()
