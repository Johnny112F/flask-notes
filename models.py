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
    Last_name = db.Column(db.String(30), nullable=False)


def connect_db(app):
    """Connect database to Flask app."""

    db.app = app
    db.init_app(app)
    