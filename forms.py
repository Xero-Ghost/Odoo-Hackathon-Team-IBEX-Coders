from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, SelectField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email Address"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=64)], render_kw={"placeholder": "First Name"})
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=64)], render_kw={"placeholder": "Last Name"})
    email = StringField('Email Address', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email Address"})
    location = StringField('Location', validators=[Optional()], render_kw={"placeholder": "Location (Optional)"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm Password"})
    agree_terms = BooleanField('I agree to the Terms of Service and Privacy Policy', validators=[DataRequired()])
    submit = SubmitField('Create Account')

class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=64)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=64)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    location = StringField('Location', validators=[Optional()])
    profile_photo = FileField('Profile Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    availability = StringField('Availability', validators=[Optional()], render_kw={"placeholder": "e.g., Weekends, Evenings (6-9 PM)"})
    is_public = BooleanField('Make Profile Public')
    submit = SubmitField('Update Profile')

class SkillForm(FlaskForm):
    name = StringField('Skill Name', validators=[DataRequired(), Length(min=2, max=100)])
    category = SelectField('Category', choices=[
        ('', 'Select Category'),
        ('design', 'Design'),
        ('development', 'Development'),
        ('marketing', 'Marketing'),
        ('business', 'Business'),
        ('languages', 'Languages'),
        ('music', 'Music'),
        ('sports', 'Sports'),
        ('cooking', 'Cooking'),
        ('photography', 'Photography'),
        ('writing', 'Writing'),
        ('other', 'Other')
    ])
    submit = SubmitField('Add Skill')

class SwapRequestForm(FlaskForm):
    skill_offered = SelectField('Skill I Offer', validators=[DataRequired()])
    skill_wanted = SelectField('Skill I Want', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[Optional()], render_kw={"placeholder": "Optional message..."})
    submit = SubmitField('Send Request')

class FeedbackForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField('Feedback', validators=[Optional()], render_kw={"placeholder": "Share your experience..."})
    submit = SubmitField('Submit Feedback')

class AdminMessageForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=200)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Send Message')

class SearchForm(FlaskForm):
    search_query = StringField('Search skills...', validators=[Optional()], render_kw={"placeholder": "Search skills..."})
    category = SelectField('Category', choices=[
        ('', 'All Categories'),
        ('design', 'Design'),
        ('development', 'Development'),
        ('marketing', 'Marketing'),
        ('business', 'Business'),
        ('languages', 'Languages'),
        ('music', 'Music'),
        ('sports', 'Sports'),
        ('cooking', 'Cooking'),
        ('photography', 'Photography'),
        ('writing', 'Writing'),
        ('other', 'Other')
    ])
    submit = SubmitField('Search')