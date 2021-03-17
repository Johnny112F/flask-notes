from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """Site user"""

    __tablename__ = "users"

    username = db.Column(db.String(20),
                         nullable=False,
                         unique=True,
                         primary_key=True,
                         )
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    notes = db.relationship("Note", backref="user")

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register a user!"""

        hashed = (bcrypt.generate_password_hash(password)
                        .decode("utf8"))

        user = cls(username=username, password=hashed, email=email,
                   first_name=first_name, last_name=last_name)

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Check for valid username and password and return user if correct"""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        return False


class Note(db.Model):
    """ User Notes"""

    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20),
                         db.ForeignKey('users.username'),
                         nullable=False
                         )


def connect_db(app):
    """Connect database to Flask app."""

    db.app = app
    db.init_app(app)
