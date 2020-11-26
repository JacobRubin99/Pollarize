from flask_wtf import FlaskForm
from models import Profile
from wtforms import BooleanField, PasswordField, StringField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms.widgets import TextArea

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
        user = Profile.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = Profile.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class CreatePollForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Create Poll')
    '''
    Do we want poll names to be unique? If yes, add this method below.

    def validate_title(self, title):
        t = Poll.query.filter_by(title=title.data).first()
        if t is not None:
            raise ValidationError('This poll name is already taken.')
    '''

class PollSearchForm(FlaskForm):
    choices = [('Author', 'Author'),
                ('Keyword', 'Keyword')]
    select = SelectField('Search for polls:', choices=choices)
    search = StringField()
    submit = SubmitField('Search')

class PollFormFactory():
    @staticmethod
    def form(choices):
        class PollForm(FlaskForm):
            new_choice = StringField('Or, add a new choice', validators=[DataRequired()])
            submit = SubmitField('Vote!')
        if choices:
            sorted_choices = sorted(choices, key=(lambda x: x.rating), reverse=True)
            choices_display = [choice.title for choice in sorted_choices]
        else:
            choices_display = ["None"]
        setattr(PollForm, 'choices', SelectField('Choices', choices=choices_display))
        return PollForm()

class AddTagFormFactory():
    @staticmethod
    def form(existing_tags):
        class AddTagForm(FlaskForm):
            tags_display = [(tag.title, tag.title) for tag in existing_tags]
            tags = SelectMultipleField(choices = tags_display)
            new_tag = StringField('Create new tag')
            submit = SubmitField('Add Tag')
        return AddTagForm()

class BioUpdateForm(FlaskForm):
    bio = StringField('New Bio', validators=[DataRequired()], widget=TextArea())
    submit = SubmitField('Save')
    cancel = SubmitField('Cancel')