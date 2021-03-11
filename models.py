"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy, ForeignKey, ForeignKeyConstraint
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(500), nullable=True, default=None)

    posts = db.relationship('Post')

    def __repr__(self):
        e = self
        return f"<User ID: {e.id} first_name: {e.first_name} last_name: {e.last_name} url: {e.image_url}>"

class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(5000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    user = db.relationship('User')

    #direct navigation: post -> post_tag & back
    post_tags = db.relationship('PostTag',
                                backref='post')

    #direct navigation: post -> tags & back
    tags = db.relationship('Tag',
                            secondary='posts_tags',
                            backref='posts')

    def __repr__(self):
        e = self
        return f"<Post ID: {e.id} title: {e.title} content: {e.content} created_at: {e.created_at} user ID: {e.user_id}>"

class Tag(db.Model):

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    #direct navigation: tag -> post & back
    posts = db.relationship('PostTag',
                            backref='tag')

    def __repr__(self):
        e = self
        return f"<User ID: {e.id} name: {e.name}>"

class PostTag(db.Model):

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['post_id', 'tag_id'],
            ['post_id.id', 'tag_id.id']
        )
    )

    def __repr__(self):
        e = self
        return f"<User ID: {e.id} name: {e.name}>"

