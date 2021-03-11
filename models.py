"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()



def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    first_name = db.Column(
        db.String(50),
        nullable=False
    )
    last_name = db.Column(
        db.String(50),
        nullable=False)
    image_url = db.Column(
        db.String(500),
        nullable=True,
        #add default, make sure it is none
    )

    post = db.relationship('Post')

class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    title = db.Column(
        db.String(50),
        nullable=False
    )
    content = db.Column(
        db.String(5000),
        nullable=False
    )
    created_at = db.Column(
        db.DateTime, 
        default=DateTime.utcnow
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )
    
    user = db.relationship('User')

