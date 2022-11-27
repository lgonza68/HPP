from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, DecimalField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    passwword = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')
    
    
class DataForm(FlaskForm):
    HouseSqFootage = IntegerField('Square Footage', validators=[DataRequired()])
    YearBuilt = IntegerField('Age', validators=[DataRequired()])
    ZipCode = StringField('Zip Code', validators=[DataRequired()])
    NumBedrooms = IntegerField('Number of Bedrooms', validators=[DataRequired()])
    NumBathrooms = DecimalField('Number of Bathrooms', validators=[DataRequired()])
    LotSize = IntegerField('Lot Size', validators=[DataRequired()])
    Basement = SelectField('Basement? (Y/N)', choices=[('Yes', 'Y'), ('No','N')], validators=[DataRequired()])
    Remodeled = SelectField('Has the house been remodeled? (Y/N)', choices=[('Yes', 'Y'), ('No','N')], validators=[DataRequired()])
    Garage = IntegerField('Number of cars that will fit in the garage. (0 = No garage)', validators=[DataRequired()])
    Pool = SelectField('Is there a pool? (Y/N)', choices=[('Yes', 'Y'), ('No','N')], validators=[DataRequired()])
    Porch = SelectField('Is there a porch? (Y/N)', choices=[('Yes', 'Y'), ('No','N')], validators=[DataRequired()])
    submit = SubmitField('Submit')
