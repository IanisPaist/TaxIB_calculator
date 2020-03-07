from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email,EqualTo, ValidationError
from application.models import Users

#registration form class
class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email', 
                    validators=[DataRequired(),Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password', 
                validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    #add additional validation of username
    def validate_username(self, username):

        #returns first if exists, None if doesn't
        user = Users.query.filter_by(username=username.data).first()
        
        #if user exists - raise error
        if user:
            raise ValidationError("Это имя занято. Пожалуйста, выберите другое")

    #add additional validation of email
    def validate_email(self,email):
        email = Users.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Этот email занят. Пожалуйста, выберите другой")


#login form class
class LoginForm(FlaskForm):
    email = StringField('Email', 
                    validators=[DataRequired(),Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember me')

    submit = SubmitField('Login') 