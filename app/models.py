from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy.types import VARCHAR
import json

class JSONEncodedDict(db.TypeDecorator):
    "Represents an immutable structure as a json-encoded string."

    impl = db.VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Annotation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    story_id = db.Column(db.Integer)
    annotation = db.Column(JSONEncodedDict)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    done = db.Column(db.Integer, default=0)

class Story(db.Model):
	__tablename__ = 'story'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(20), unique=True)
	description = db.Column(db.String(200))
	syllables = db.relationship('Syllable')
	

class Syllable(db.Model):
	__tablename__ = 'syllable'
	id = db.Column(db.Integer, primary_key=True)
	story_id = db.Column(db.Integer, db.ForeignKey(Story.id), 
	nullable=False, index=True)
	frag_nbr = db.Column(db.SmallInteger, nullable=False)
	line_nbr = db.Column(db.SmallInteger, nullable=False)
	word_nbr = db.Column(db.SmallInteger, nullable=False)
	syll_nbr = db.Column(db.SmallInteger, nullable=False)
	syllable = db.Column(db.String(30), nullable=False)


class Annotation_new(db.Model):
	__tablename__ = 'annotation_new'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey(User.id), index=True)
	syllable_id = db.Column(db.Integer, db.ForeignKey(Syllable.id), 
	nullable=False)
	stressed = db.Column(db.Boolean, default=False)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)
	fragment_done = db.Column(db.Boolean, default=False)


