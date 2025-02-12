from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from referencecreator.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content_type = RadioField('Content type', validators=[DataRequired()], choices=[('plain', 'Plain Text'), ('html', 'HTML'), ('markdown', 'Markdown')])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class ProjectForm(FlaskForm):  # Project form --> create new project
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Create new project')


class ReferenceForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    subtitle = StringField('Subtitle')
    reference_type = RadioField('Reference type', validators=[DataRequired()], choices=[('book', 'Book'), ('paper', 'Academic paper'), ('other', 'Other')])
    publish_date = StringField('Publish date')
    author = StringField('Author(s)')
    volume = IntegerField('Volume')
    number = IntegerField('Number')
    pages = StringField('Pages')
    doi = StringField('doi')
    isbn = StringField('ISBN')
    chapter = StringField('Chapter(s)')
    editor = StringField('Editor')
    publish_place = StringField('Publish place')
    publisher = StringField('Publisher')
    url = StringField('url')
    organisation = StringField('Organisation')
    submit = SubmitField('Add reference')

