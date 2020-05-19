from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from project1 import db

# Association table between Books and Users
class Review(db.Model):
    book_id = db.Column(db.String(25), db.ForeignKey('book.id'), primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    review = db.Column(db.Text)
    rating = db.Column(db.Float)

    books = db.relationship("Book", back_populates="users")
    users = db.relationship("User", back_populates="books")

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(25), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(25), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    count_ratings = db.Column(db.Integer)
    overall_rating = db.Column(db.Float)

    users = db.relationship("Review", back_populates="books")


# User table to hold all of the users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(25), nullable=False)

    books = db.relationship("Review", back_populates="users")
