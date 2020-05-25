from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from project1 import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Association table between Books and Users
class Review(db.Model):
    book_id = db.Column(db.String(25), db.ForeignKey('book.id'), primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    username = db.Column(db.String(25), nullable=False)
    bookname = db.Column(db.String(50), nullable=False)
    review = db.Column(db.Text)
    rating = db.Column(db.Float)

    books = db.relationship("Book", back_populates="reviews")
    users = db.relationship("User", back_populates="reviews")

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(25), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(25), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    count_ratings = db.Column(db.Integer)
    overall_rating = db.Column(db.Float)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    reviews = db.relationship("Review", back_populates="books")


# User table to hold all of the users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    reviews = db.relationship("Review", back_populates="users")
