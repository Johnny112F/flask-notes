from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import RegisterForm, LoginForm

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

        return redirect("/users/secret")

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
            return redirect("/secret")
        form.username.errors = ["Invalid Input. Try Again"]
        return render_template("users/login.html", form=form)

    return render_template("users/login.html", form=form)


@app.route("/logout")
def logout():
    """logout user"""

    session.pop("username")
    return redirect("/login")



