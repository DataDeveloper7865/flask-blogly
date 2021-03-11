"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post

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
    posts = user.posts

    return render_template("user-detail.html", user=user, posts=posts)

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

@app.route("/users/<int:userid>/posts/new")
def add_a_post_from_user(userid):
    """Show form to add a post for that user."""
    user = User.query.get_or_404(userid)

    return render_template("new-post.html", user=user)

@app.route("/users/<int:userid>/posts/new", methods=["POST"])
def handle_add_a_post(userid):
    """Handle add form; add post and redirect to the user detail page."""

    title = request.form['title']
    content = request.form['post-content']

    post_to_add = Post(title=title, content=content, user_id=userid)

    db.session.add(post_to_add)

    db.session.commit()

    return redirect(f"/users/{userid}")

@app.route("/posts/<int:postid>")
def show_a_post(postid):
    """ Show a post.
    Show buttons to edit and delete the post.
    """
    post = Post.query.get_or_404(postid)

    return render_template("post-detail.html", post=post)

@app.route("/posts/<int:postid>/edit")
def show_form_to_edit_post(postid):
    """ Show form to edit a post, and to cancel (back to user page).
    """
    post = Post.query.get_or_404(postid)

    return render_template("post-edit.html", post=post)

@app.route("/posts/<int:postid>/edit", methods=["POST"])
def handle_editing_of_post(postid):
    """Handle editing of a post. Redirect back to the post view"""

    post_to_edit = Post.query.get_or_404(postid)

    new_title = request.form["title"]
    new_content = request.form["post-content"]

    post_to_edit.title = new_title
    post_to_edit.content = new_content

    db.session.commit()

    return redirect(f"/posts/{postid}")

@app.route("/posts/<int:postid>/delete", methods=["POST"])
def delete_a_post(postid):
    """ Delete the post passed in """
    post_to_delete = Post.query.get_or_404(postid)
    user_return_id = post_to_delete.user_id
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(f"/users/{user_return_id}")












