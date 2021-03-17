from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Note
from forms import RegisterForm, LoginForm, NoteForm
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask_notes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "hello-secrets"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def home():
    """Direct user to home page of the site, then redirect for registration"""

    return redirect("/register")


@app.route('/register', methods=["GET", "POST"])
def register():
    """Produce a form to register a user and handle form submission"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")
    
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)
        
        db.session.commit()
        session['username'] = user.username

        return redirect(f"/users/{user.username}")

    else:
        return render_template("users/register.html", form=form)


@app.route("/secret")
def secret():
    """User is redirected to secret.html upon completing form successfully"""
    # check for user in session
    if "username" in session:
        return render_template("/users/secret.html")
    else:
        return "incorrect login"


@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form and handle login"""
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        form.username.errors = ["Invalid Input. Try Again"]
        return render_template("users/login.html", form=form)

    return render_template("users/login.html", form=form)


@app.route("/logout")
def logout():
    """logout user"""

    session.pop("username")
    return redirect("/login")


@app.route("/users/<username>")
def show_user(username):
    """Show user info when logged in"""

    user = User.query.get(username)

    return render_template("users/show.html", user=user)


@app.route("/users/<username>/notes/new", methods=["GET", "POST"])
def new_note(username):
    """Show add-note form and process it"""

    form = NoteForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

    #make an instance of Note
        note = Note(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(note)
        db.session.commit()

        return redirect(f"/users/{note.username}")
    return render_template("/notes/new.html", form=form)


@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    """Remove user and redirect to login."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    Note.query.filter_by(username=username).delete()
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")


@app.route("/notes/<int:note_id>/update", methods=["GET", "POST"])
def update_note(note_id):
    """Show update-note form and process it."""

    note = Note.query.get(note_id)

    if "username" not in session or note.username != session['username']:
        raise Unauthorized()

    form = NoteForm(obj=note)

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{note.username}")

    return render_template("/notes/edit.html", form=form, feedback=note)


@app.route("/notes/<int:note_id>/delete", methods=["POST"])
def delete_note(note_id):
    """Delete note."""

    note = Note.query.get(note_id)
    if "username" not in session or note.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():   # <-- csrf checking!
        db.session.delete(note)
        db.session.commit()

    return redirect(f"/users/{note.username}")

