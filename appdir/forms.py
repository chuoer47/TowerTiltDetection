from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Regexp


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],
                           render_kw={'class': 'form-control'})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={'class': 'form-control'})
    repassword = PasswordField('Repeat Password', validators=[DataRequired()],
                               render_kw={'class': 'form-control'})
    submit = SubmitField('Register', render_kw={'class': 'btn btn-outline-primary', 'id': 'submit'})


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],
                           render_kw={'class': 'form-control'})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={'class': 'form-control'})
    submit = SubmitField('Login', render_kw={'class': 'btn btn-outline-primary', 'id': 'submit'})


class AnswerForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()],
                            render_kw={'class': 'form-control', 'id': 'answer-content'})
    submit = SubmitField('Post', render_kw={'class': 'btn btn-outline-primary', 'id': 'submit-answer'})
