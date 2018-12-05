from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy.types import VARCHAR
import json


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    language = db.Column(db.SmallInteger)
    middledutch = db.Column(db.SmallInteger)
    

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Story(db.Model):
	__tablename__ = 'story'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(20), unique=True)
	description = db.Column(db.String(200))
	fragments = db.relationship('Fragment', lazy='dynamic')
	
	def __repr__(self):
		return "<Story %r>" % self.title

class Fragment(db.Model):
	__tablename__ = 'fragment'
	id = db.Column(db.Integer, primary_key=True)
	story_id = db.Column(db.Integer, db.ForeignKey(Story.id),\
		nullable=False, index=True)
		
	def get_all_ids():
		res = db.engine.execute("select id from fragment")
		ids = res.fetchall()
		idsl = [ id[0] for id in ids ]
		return idsl
		
	def get_story_description(frag_id):
		res = db.engine.execute('select description from fragment join \
		story on (story.id = fragment.story_id) where fragment.id=?', (frag_id,))
		descr = res.fetchone()
		return descr[0]
		
		
	def __repr__(self):
		return "Fragment %r story %r" % (self.id, self.story_id)

class Syllable(db.Model):
	__tablename__ = 'syllable'
	id = db.Column(db.Integer, primary_key=True)
	frag_id = db.Column(db.Integer, db.ForeignKey(Fragment.id),\
		nullable=False, index=True)
	frag_nbr = db.Column(db.SmallInteger, nullable=False)
	line_nbr = db.Column(db.SmallInteger, nullable=False)
	word_nbr = db.Column(db.SmallInteger, nullable=False)
	syll_nbr = db.Column(db.SmallInteger, nullable=False)
	syllable = db.Column(db.String(30), nullable=False)

	def __repr__(self):
		return "<Syllable %r %r %r %r %r>" % (self.frag_nbr, self.line_nbr, \
		self.word_nbr, self.syll_nbr, self.syllable)
		
	#returns nbr lines in a fragment
	@staticmethod
	def nbr_lines(frag_id):
		res = db.engine.execute('select max(line_nbr) from syllable where \
		frag_id = ?', (frag_id,))
		lines = res.fetchone()
		return lines[0]

	#returns nbr words in a line in a fragment
	@staticmethod
	def nbr_words(frag_id, line_nbr):
		res = db.engine.execute('select max(word_nbr) from syllable where \
		frag_id = ? and line_nbr = ?', (frag_id, line_nbr))
		lines = res.fetchone()
		return lines[0]
		
				 
	#convert the fragment in the database to a list of lists of lists of
	#dictionaries(frag->lines->line->words->word->syllables  	
	@staticmethod
	def convert_to_list(frag_id):
		nbr_lines = Syllable.nbr_lines(frag_id)
		if nbr_lines:
			lines_list=[]
			for line_idx in range(1, nbr_lines + 1): 
				nbr_words = Syllable.nbr_words(frag_id, line_idx)				
				line_list=[]
				for word_idx in range(1, nbr_words + 1):
					syls = Syllable.query.filter_by(frag_id=frag_id, \
					line_nbr = line_idx, word_nbr = word_idx).all()
					word_list=[]
					for syl in syls:
						sdict = dict(id=syl.id, text=syl.syllable)
						word_list.append(sdict)
					line_list.append(word_list)
				lines_list.append(line_list)
		return lines_list

		
class Annotation(db.Model):
	__tablename__ = 'annotation'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey(User.id), index=True)
	syllable_id = db.Column(db.Integer, db.ForeignKey(Syllable.id), 
	nullable=False)
	stressed = db.Column(db.Boolean, default=False)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)
	fragment_done = db.Column(db.Boolean, default=False)
	fragment = db.relationship('Syllable')

	def get_fragments_done(user_id):
		res = db.engine.execute("select frag_id from annotation inner \
		join syllable  on (syllable.id = annotation.syllable_id) where \
		fragment_done and user_id = ? group by frag_id", (user_id));
		frag_done = res.fetchall()
		frag_done_l = [frag[0] for frag in frag_done]
		return frag_done_l
