from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, SelectField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from app.models import User, Annotation


class LoginForm(FlaskForm):
    username = StringField('Gebruikersnaam', validators=[DataRequired()])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    remember_me = BooleanField('Onthoud mij')
    submit = SubmitField('Aanmelden')


class RegistrationForm(FlaskForm):
    username = StringField('Gebruikersnaam', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    password2 = PasswordField(
        'Herhaal wachtwoord', validators=[DataRequired(), EqualTo('password')])
    language = RadioField('Moedertaal', choices = [('vlaams', 'Vlaams'), 
      ('nederlands', 'Nederlands')])
    middledutch = RadioField('Hoe schat u uw kennis in van het Middelnederlands?', choices = [('geen', 'Geen'), 
      ('gemiddeld', 'Gemiddeld'), ('goed', 'Goed')])
    submit = SubmitField('Registreer')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
