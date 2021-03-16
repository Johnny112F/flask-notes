from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email

# class LoginForm(FlaskForm):
#     """Login Form."""


class RegisterForm(FlaskForm):
    """Registration Form."""

    username = StringField("Username", validators=[InputRequired(),
                                                   Length(min=8, max=20)], )
    password = PasswordField("Password", validators=[InputRequired(),
                                                     Length(min=5, max=55)], )
    email = StringField("Email", validators=[InputRequired(), Email(),
                                             Length(max=50)], )
    first_name = StringField("Username", validators=[InputRequired(),
                                                     Length(max=20)], )
    last_name = StringField("Username", validators=[InputRequired(),
                                                    Length(max=20)], )
