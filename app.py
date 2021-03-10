"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Jayjayiscool1@127.0.0.1/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

@app.route("/")
def show_users():
    """ Redirect to list of users """

    return redirect("/users")

@app.route("/users")
def show_all_users():
    """ Show all users """
    users = User.query.all()
    return render_template("user-listing.html", users=users)

@app.route("/users/new")
def create_new_user():
    """ show an add form for users"""

    return render_template("create-user.html")

@app.route("/users/new", methods=["POST"])
def handle_new_user_creation():
    """ Process the add form, adding a new user and going back to /users"""

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    img_url = request.form['image-url']

    user = User(first_name = first_name, last_name = last_name, image_url = img_url)
    db.session.add(user)
    db.session.commit()
    
    return redirect("/users")

@app.route("/users/<int:userid>")
def get_info_for_user():
    """ show infomration about the given user. Have a button to get to their edit page, and to 
    delete the user."""

    return render_template("user-detail.html")

@app.route("/users/<int:userid>/edit")
def edit_a_user():
    """ Show the edit page for the user.
    Have a cancel button that returns to the detail page for a user,
    and a save button that updates the user. """

    render_template("user-edit.html", user=user)


@app.route("/users/<int:userid>/edit", methods=["POST"])
def process_edit_user():
    """Process the edit form, returning the user to the /users page"""


    return redirect("/users")

@app.route("/users/<int:userid>/delete", methods=["POST"])
def delete_a_user(userid):

    return redirect("/users")







