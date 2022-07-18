from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField, SubmitField, TextAreaField, SelectMultipleField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms.widgets import HiddenInput
from app.models import User, Tag, Entry


class LoginForm(FlaskForm):
    email = StringField('Email Adresse', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    submit = SubmitField('Anmelden')


class RegistrationForm(FlaskForm):
    username = StringField('Benutzername*', validators=[DataRequired()])
    firstname = StringField('Vorname')
    lastname = StringField('Nachname')
    email = StringField('Email*', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort*', validators=[DataRequired()])
    password2 = PasswordField('Passwort wiederholen*',
                              validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrieren')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(
                'Bitte verwenden Sie einen anderen Benutzernamen.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(
                'Bitte verwenden Sie eine andere Email Adresse.')


class AddEntryForm(FlaskForm):
    choices = []
    tagList = Tag.query.all()
    for tag in tagList:
        choices.append((tag.id, tag.description))

    title = StringField("Titel", validators=[DataRequired()])
    content = TextAreaField("Inhalt", validators=[DataRequired()])
    tags = SelectMultipleField('Tags', coerce=int, choices=choices)
    submit = SubmitField("Erstellen")

    def validate_title(self, title):
        entry = Entry.query.filter_by(title=title.data).first()
        if entry is not None:
            raise ValidationError('Bitte verwenden Sie einen anderen Titel.')


class AddCommentForm(FlaskForm):
    content = TextAreaField("Kommentar", validators=[DataRequired()], render_kw={
                            "placeholder": "Bitte einen Kommentar abgeben"})
    entry_id = IntegerField("EntryId")
    submit = SubmitField("Eingeben")


class EditEntryForm(FlaskForm):
    choices = []
    tagList = Tag.query.all()
    for tag in tagList:
        choices.append((tag.id, tag.description))

    title = StringField("Titel", validators=[DataRequired()])
    content = TextAreaField("Inhalt", validators=[DataRequired()])
    tags = SelectMultipleField('Tags', coerce=int, choices=choices)
    submit = SubmitField("Bearbeiten")
