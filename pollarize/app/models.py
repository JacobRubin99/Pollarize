from flask_login import UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

migrate = Migrate()
db = SQLAlchemy()

# user_id, email, password, username, bio, score
# UserMixin specifies get_id, etc.
class Profile(db.Model, UserMixin):
    __tablename__ = 'profile'
    id = db.Column('id', db.Integer(), primary_key=True)
    email = db.Column('email', db.String(50))
    password = db.Column('password', db.String(128))
    username = db.Column('username', db.String(20))
    bio = db.Column('bio', db.Text())
    score = db.Column('score', db.Integer())

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# (poll_id, title, dateAdded, creator_user_id [-> User.user_id]
class Poll(db.Model):
    __tablename__ = 'poll'
    poll_id = db.Column('id', db.Integer(), primary_key=True)
    title = db.Column('title', db.String(300))
    date_added = db.Column('date_added', db.Date())
    creator_user_id = db.Column(db.Integer(), db.ForeignKey('profile.id'))

# poll_id [-> Poll.poll_id], title, date_added, creator_user_id [-> User.user_id], rating
class Choice(db.Model):
    __tablename__ = 'choice'
    id = db.Column('id', db.Integer(), primary_key=True)
    poll_id = db.Column('poll_id', db.Integer(), db.ForeignKey('poll.id'))
    title = db.Column('title', db.String(300))
    date_added = db.Column('date_added', db.Date())
    creator_user_id = db.Column(db.Integer(), db.ForeignKey('profile.id'))
    rating = db.Column('rating', db.Integer())

class Vote(db.Model):
    __tablename__ = 'vote'
    choice_id = db.Column('choice_id', db.Integer(), db.ForeignKey('choice.id'), primary_key=True)
    user_id = db.Column('profile', db.Integer(), db.ForeignKey('profile.id'), primary_key=True)
    value = db.Column('value', db.Integer(), db.CheckConstraint('value<2'),  db.CheckConstraint('value>-2'))

class Tag(db.Model):
    __tablename__ = 'tag'
    title = db.Column('title', db.String(300), primary_key=True)
    date_added = db.Column('date_added', db.Date())
    creator_user_id = db.Column(db.Integer(), db.ForeignKey('profile.id'))

class PollTag(db.Model):
    __tablename__ = 'polltag'
    poll_id = db.Column('poll_id', db.Integer(), db.ForeignKey('poll.id'), primary_key=True)
    tag_title = db.Column('tag_title', db.String(300), db.ForeignKey('tag.title'), primary_key=True)