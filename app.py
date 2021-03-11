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
def get_info_for_user(userid):
    """ show infomration about the given user. Have a button to get to their edit page, and to 
    delete the user."""

    user = User.query.get_or_404(userid)

    return render_template("user-detail.html", user=user)

@app.route("/users/<int:userid>/edit")
def edit_a_user(userid):
    """ Show the edit page for the user.
    Have a cancel button that returns to the detail page for a user,
    and a save button that updates the user. """

    user = User.query.get_or_404(userid)

    return render_template("user-edit.html", user=user)


@app.route("/users/<int:userid>/edit", methods=["POST"])
def process_edit_user(userid):
    """Process the edit form, returning the user to the /users page"""

    user_to_edit = User.query.get(userid)

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    img_url = request.form['image-url']

    user_to_edit.first_name = first_name
    user_to_edit.last_name = last_name
    user_to_edit.img_url = img_url

    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:userid>/delete", methods=["POST"])
def delete_a_user(userid):
    """Delete the user from the database, and return"""

    user_to_delete = User.query.get(userid)

    db.session.delete(user_to_delete)

    db.session.commit()

    return redirect("/users")







