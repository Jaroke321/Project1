from flask import session, render_template, request, redirect, url_for, flash
from project1.models import Book, User, Review
from project1 import app
from project1.forms import RegistrationForm, LoginForm
import csv

from project1 import db

# Route to the main homepage
@app.route("/")
def index():
    """Default page"""

    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    """Login page"""

    form = LoginForm()  # Create the wtf form to pass to template

    # User submitted credentials
    if form.validate_on_submit():
        # Grab the input from the user
        name = request.form.get("username")
        password = request.form.get("password")
        # See if the input matches any records
        user = User.query.filter_by(name=name, password=password).first()
        # Credentials do not exist
        if user is None:
            # Create flash error message and send user back to login
            flash('Username or Password is Incorrect', 'danger')
            return render_template('login.html', title="Login Page",
                form=form)
        else: # Success
            return redirect(url_for('index'))
    # GET request
    else:
        return render_template('login.html', title="Login Page", form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    """Used to register a new user"""

    # Create the form
    form = RegistrationForm()
    # Validate the form
    if form.validate_on_submit():
        # Grab the username the user entered
        username = request.form.get("username")
        # Query database for username
        check_name = User.query.filter_by(name=username).first()
        # Check if username is taken
        if check_name is None:
            # Grab the password and create the user
            pass1 = request.form.get("password")
            user = User(name=username, password=pass1)
            db.session.add(user)
            db.session.commit()

            # Create success flash message and send user to home screen
            flash(f"Successfully Created Account For {username}", 'success')
            return redirect(url_for('index'))

        else:
            flash(f'Username Is Taken', 'danger')
            return render_template('register.html', title="Register",
                form=form)

    else:
        return render_template('register.html', title="Register", form=form)

@app.route("/profile/<int:id>")
def profile(id):
    """Loads the books and reviews of a specific user
    given the user id"""

    # Get the correct user
    user = User.query.get(id)
    return render_template('profile.html', username=user.name)


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
