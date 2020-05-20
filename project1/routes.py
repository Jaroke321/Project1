from flask import session, render_template, request, redirect, url_for
from project1.models import Book, User, Review
from project1 import app
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

    # User submitted credentials
    if request.method == 'POST':

        # Grab the input from the user
        name = request.form.get("username")
        password = request.form.get("password")

        # See if the input matches any records
        user = User.query.filter_by(name=name, password=password).first()

        # Credentials do not exist
        if user is None:
            return render_template('login.html', title="Login Page",
                heading="Login", msg="Username or Password is incorrect")
        else:
            return redirect(url_for('profile', id=user.id))
    else:
        return render_template('login.html', title="Login Page", heading="Login")

@app.route("/register", methods=['GET', 'POST'])
def register():
    """Used to register a new user"""

    if request.method == 'POST':

        username = request.form.get("name")
        # Confirm username is valid
        check_name = User.query.filter_by(name=username).first()
        # Username does not yet exist
        if check_name is None:
            # Check that the passwords matches
            pass1 = request.form.get("password")
            pass2 = request.form.get("confirm_password")

            # Passwords match
            if pass1 == pass2:
                # Add the user to the database
                new_user = User(name=username, password=pass1)
                db.session.add(new_user)
                db.session.commit()

                # Redirect to the new users profile Page
                return redirect(url_for('profile', id=new_user.id))
            # The passwords did not match
            else:
                return render_template('register.html', title="Register",
                    heading="Register", msg="Passwords do not match")
        # This username already exists
        else:
            return render_template('register.html', title="Register",
                heading="Register", msg="This username already exists")

    else:
        return render_template('register.html', title="Register", heading="Register")

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
