from flask import session, render_template, request, redirect, url_for, flash, jsonify
from project1.models import Book, User, Review
from project1 import app, bcrypt, db
from project1.forms import RegistrationForm, LoginForm, UpdateAccountForm, ReviewForm
from flask_login import login_user, current_user, logout_user, login_required
import csv, secrets, os
from sqlalchemy import func, desc

# Route to the main homepage
@app.route("/")
def index():
    """Ths route is the default route, or homepage.
    It will list all of the books in the data base, and
    allow users to see some information on those books
    as well as allow users to click and navigate to that books page."""

    books = Book.query.all()  # Get all of the books from the database

    # Render the home page
    return render_template('home.html', books=books)

@app.route("/login", methods=['GET', 'POST'])
def login():
    """Login page"""

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()  # Create the wtf form to pass to template

    # User submitted credentials
    if form.validate_on_submit():
        # Grab the input from the user
        name = request.form.get("username")
        # See if the input matches any records
        user = User.query.filter_by(name=name).first()
        # Credentials do not exist
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # Success
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        # Unsuccessful
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    # GET request
    else:
        return render_template('login.html', title="Login Page", form=form)

@app.route("/logout")
@login_required
def logout():
    # Logout user
    logout_user()
    # Redirect user to the login page
    return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    """Used to register a new user"""

    if current_user.is_authenticated:
        redirect(url_for('index'))

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
            pass1 = bcrypt.generate_password_hash(request.form.get("password")).decode('utf-8')
            user = User(name=username, password=pass1)
            db.session.add(user)
            db.session.commit()

            # Create success flash message and send user to home screen
            flash(f"Successfully Created Account For {username}", 'success')
            return redirect(url_for('login'))

        else:
            flash(f'Username is taken. Please choose a different one.', 'danger')
            return render_template('register.html', title="Register",
                form=form)

    else:
        return render_template('register.html', title="Register", form=form)

def savePicture(form_picture):

    # Create a random path
    random_hex = secrets.token_hex(8)
    # Separate the file extension and append the extension to the hex value
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # Get the complete path for the picture to be saved to
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path) # Save the picture to file with the hexed name

    return picture_fn


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    """Loads the books and reviews of a specific user
    given the user id"""

    # Load the update form
    form = UpdateAccountForm()
    review_count = len(current_user.reviews)
    # Proceed if the validators are satisfied
    if form.validate_on_submit():
        if form.picture.data: # if the user updated their profile pic
            picture_fn = savePicture(form.picture.data) # Save pic and get path
            current_user.image_file = picture_fn # Set the users image_file with the new value
            flash(f'Your Profile Picture Has Been Successfully Updated', 'success')
            db.session.commit() # Commit changed to the db

        # User is attempting to update there username
        if (form.username.data != current_user.name) and (User.query.filter_by(name=form.username.data).first() is None):
            # Update the username
            current_user.name = form.username.data
            db.session.commit()
            flash(f'Your Username Has Been Updated Successfully', 'success')
        else:
            flsh(f'Sorry, that username is already taken', 'danger')

    # Get the image file associated with the user
    img_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    form.username.data = current_user.name
    # Load the profile page with the image file
    return render_template('profile.html', img_file=img_file, form=form,
        count=review_count)

@app.route("/user/<int:id>")
def users(id):
    """Displays the information and the review data of a user
    given that users id. This is used so that users can view
    other users profiles and see the reviews that they have left."""

    user = User.query.get(int(id))  # Get the user with the id of id
    # Get the users profile picture
    img_file = url_for('static', filename=f'profile_pics/{user.image_file}')
    user_prof = False  # Used to determine if the user page is the current users page
    # See if the current user is navigating to their own page
    if current_user.id == id:
        user_prof = True

    review_count = len(user.reviews) # Holds the number of reviews for the user
    activity_list = []               # Used for the recent activity section for the user
    count = 0                        # Used to limit the amount of activities to 5

    while ((count < 5) and (count < review_count)):
        activity_list.append(user.reviews[-(count+1)])
        count += 1

    reviews = Review.query.filter_by(user_id=user.id).order_by(desc(Review.timestamp)).all()

    # Render the template
    return render_template('user.html', user=user,
        count=review_count, img=img_file, user_prof=user_prof,
        activity_list=activity_list, reviews=reviews)

@app.route('/review/<int:id>', methods=['GET', 'POST'])
@login_required
def review(id):
    """Produces a form so that a user can leave a new review for a
    book. The id parameter is the id associated with a specific book."""

    form = ReviewForm()            # Create the form
    book = Book.query.get(int(id)) # Get the book from the database

    # Attempts to grab a review of this book by this user
    r = Review.query.filter_by(book_id=id, user_id=current_user.id).first()
    heading = "New" # Used as aheading in the HTML

    if book is None:  # Check that the book exists
        flash('That Book ID Is Invalid', 'info')
        redirect(url_for('index'))

    # User has hit the submit button
    if form.validate_on_submit() and form.submit.data:  # User submitted the form
        new_review = Review(book_id=id, user_id=current_user.id,
            username=current_user.name, bookname=book.title,
            review=form.review.data, rating=form.rating.data)

        # Delete the past review before adding the new one
        if r:
            db.session.delete(r)
            db.session.commit()

        db.session.add(new_review)  # Add new review
        db.session.commit()         # Commit changes to the database
        flash('Review Was Successfully Added', 'success')  # flash message
        # Redirect to home Page
        return redirect(url_for('book', id=book.id))

    # If user has already left a review but has not submited the form yet
    if r:
        # Fill in the form data with the users past review of this book
        form.review.data = r.review
        form.rating.data = r.rating
        heading = "Update"

    # The user has made a review previously and hit the delete button
    if form.delete.data and r:
        db.session.delete(r)
        db.session.commit()
        flash(f'Your Review Was Successfully Deleted', 'success')
        # Take the user back to their user page
        return redirect(url_for('users', id=current_user.id))
    # Render the review template
    return render_template('review.html', heading=heading, form=form, book=book)

@app.route("/api/book/<int:book_id>")
def apiBook(book_id):
    """This method is an api method for this web application.
    It allows other developers to access the database and get a
    specific book and its data given that books id. Data is
    presented in standard JSON format"""

    # Grab the book from the data base
    book = Book.query.filter_by(id=f'{book_id}').first()
    # Return error if book is None
    if book is None:
        return jsonify({"error": "Invalid book name"}), 422

    # Get all of the reviews for the book
    rs = book.reviews
    # Create lists to store all of the individual ratings and reviews
    reviews = []
    ratings = []
    users = []

    # Cycle through the reviews and append reviews and ratings to the lists
    for review in rs:
        reviews.append(review.review)
        ratings.append(review.rating)
        users.append(review.username)

    return jsonify({
        "isbn": book.isbn,
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "ratings": ratings,
        "reviews": reviews,
        "users": users
        })


def getApi():
    """This method allows the web application to
    grab information from the goodreads API."""



@app.route("/book/<int:id>")
def book(id):
    """This method loads the information for a single book.
    This includes title, isbn number, year published, as well
    as all of the review information for that book"""

    book = Book.query.get(int(id)) # Get the book from the database
    # Get the books picture from the static folder
    img_file = url_for('static', filename=f'book_pics/{book.image_file}')
    reviewed = False  # used to see if the user has reviewed this book

    if Review.query.filter_by(book_id=id, user_id=current_user.id).first():
        reviewed = True

    return render_template('book.html', book=book, img=img_file,
        reviewed=reviewed)


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

    temp_pass = bcrypt.generate_password_hash("password").decode('utf-8')

    ## Add some users
    user1 = User(name="Jaroke", password=temp_pass)
    user2 = User(name="BenW", password=temp_pass)
    user3 = User(name="EricKatz", password=temp_pass)
    # Add users to the database
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)

    # Add some reviews
    r1 = Review(book_id=1, user_id=1, username=user1.name,
        bookname="Krondor: The Betrayal", review="Good Book", rating=4.5)
    r2 = Review(book_id=1, user_id=2, username=user2.name,
        bookname="Krondor: The Betrayal", review="OK book", rating=3)
    r3 = Review(book_id=2, user_id=1, username=user1.name,
        bookname="The Dark Is Rising", review="Not good", rating=2)
    # Add reviews to the database
    db.session.add(r1)
    db.session.add(r2)
    db.session.add(r3)

    #Commit Changes
    db.session.commit()
