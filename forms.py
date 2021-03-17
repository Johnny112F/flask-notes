from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, Email, NumberRange, Email, Optional
from flask_wtf import FlaskForm

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
    first_name = StringField("First Name", validators=[InputRequired(),
                                                       Length(max=20)], )
    last_name = StringField("Last Name", validators=[InputRequired(),
                                                     Length(max=20)], )


class LoginForm(FlaskForm):
    """Login Form"""
    username = StringField("Username", validators=[InputRequired(),
                                                   Length(min=8, max=20)], )
    password = PasswordField("Password", validators=[InputRequired(),
                                                     Length(min=5, max=55)], )


class NoteForm(FlaskForm):
    """Add feedback form."""

    title = StringField(
        "Title",
        validators=[InputRequired(), Length(max=100)],
    )
    content = TextAreaField(
        "Content",
        validators=[InputRequired()],
        render_kw={'class': 'form-control', 'rows': 10}
    )


class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""
