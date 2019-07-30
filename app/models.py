from datetime import datetime
from app import db, login
from flask_login import UserMixin
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
import random
from sqlalchemy.types import VARCHAR
import json
import pprint
import csv
import pickle


class User(UserMixin, db.Model):
    """ User information for account login """
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
        """set the password for the user"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """check a given passord for a user"""
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    """load a user with a specific id"""
    return User.query.get(int(id))

class Story(db.Model):
    """a story consistes of 1 or more fragments"""
    __tablename__ = 'story'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True)
    description = db.Column(db.String(200))
    fragments = db.relationship('Fragment', lazy='dynamic')

    def __repr__(self):
        return "<Story %r>" % self.title
    
    @staticmethod
    def get_nbr_of_stories():
        res = db.engine.execute('select count(*) from story')
        return res.fetchone()[0]

    #we only take 5 elements of the list, otherwise their seems to a sort
    #of overflow in fadein....
    def all_descriptions():
        res = db.session.execute('select description from story')
        descr = res.fetchall()
        descrl = [des[0] for des in descr]
        return random.sample(descrl,5)

class Fragment(db.Model):
    """a fragment will be presented to the user for a scansession"""
    __tablename__ = 'fragment'
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey(Story.id),\
                         nullable=False, index=True)
    frag_nbr = db.Column(db.SmallInteger, nullable=False)

    def get_all_ids():
        """get a list of all fragment id's"""
        res = db.engine.execute("select id from fragment")
        ids = res.fetchall()
        idsl = [id[0] for id in ids]
        return idsl

    def get_story_description(frag_id):
        """whats the escription of the story of this fragment"""
        res = db.engine.execute('select description from fragment join \
        story on (story.id = fragment.story_id) where fragment.id=?', (frag_id,))
        descr = res.fetchone()
        return descr[0]
    
    @staticmethod
    def get_nbr_of_fragments():
        res = db.engine.execute('select count(*) from fragment')
        return res.fetchone()[0]

    def __repr__(self):
        return "Fragment %r story %r" % (self.id, self.story_id)

class Syllable(db.Model):
    """a fragment contains several lines of words, each word is composed
    by syllables. In a scansession, the user can select a syllable which
    ca be stressed (or not"""
    __tablename__ = 'syllable'
    id = db.Column(db.Integer, primary_key=True)
    frag_id = db.Column(db.Integer, db.ForeignKey(Fragment.id),\
                        nullable=False, index=True)
    #frag_nbr = db.Column(db.SmallInteger, nullable=False)
    line_nbr = db.Column(db.SmallInteger, nullable=False)
    word_nbr = db.Column(db.SmallInteger, nullable=False)
    syll_nbr = db.Column(db.SmallInteger, nullable=False)
    syllable = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return "<Syllable %r %r %r %r %r>" % (self.frag_nbr, self.line_nbr, \
                                              self.word_nbr, self.syll_nbr, \
                                              self.syllable)

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
    #lolg -> list of lists
    @staticmethod
    def convert_to_list(frag_id, lol=False):
        nbr_lines = Syllable.nbr_lines(frag_id)
        if nbr_lines:
            lines_list = []
            for line_idx in range(1, nbr_lines + 1):
                nbr_words = Syllable.nbr_words(frag_id, line_idx)
                line_list = []
                for word_idx in range(1, nbr_words + 1):
                    syls = Syllable.query.filter_by(frag_id=frag_id, \
                                                    line_nbr=line_idx, \
                                                    word_nbr=word_idx).all()
                    word_list = []
                    for syl in syls:
                        if(not lol):
                            sdict = dict(id=syl.id, text=syl.syllable)
                        else:
                            sdict = syl.syllable
                        word_list.append(sdict)
                    line_list.append(word_list)
                lines_list.append(line_list)
        return lines_list

    def get_frag_id(syl_id):
        res = db.engine.execute("select frag_id from syllable where id = ?", (syl_id))
        return res.fetchone()[0]

class Annotation(db.Model):
    """all the annotation of a user for the different syllables 
    of a fragment of a story"""
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
        fragment_done and user_id = ? group by frag_id", (user_id))
        frag_done = res.fetchall()
        frag_done_l = [frag[0] for frag in frag_done]
        return frag_done_l

class Scanned(db.Model):
    """all the complete scanned feragments of a user"""
    __tablename__ = 'fragmentdone'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), index=True)
    frag_id = db.Column(db.Integer, db.ForeignKey(Fragment.id),\
                        nullable=False, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def get_frag_maxfreq():
        """ get all fragments that reached their maximum scan frequency """
        res = db.engine.execute("select frag_id from fragmentdone group by frag_id \
        having count(*) = ?", (current_app.config["MAX_SCANS_FRAGMENT"]))
        frag_max_freq = res.fetchall()
        frag_max_freq_l = [frag[0] for frag in frag_max_freq]
        return frag_max_freq_l
        
    def get_frag_done(user_id):
        """ get the fragments done by a specific user """
        res = db.engine.execute("select frag_id from fragmentdone where user_id = ?", (user_id))
        frag_done = res.fetchall()
        frag_done_l = [frag[0] for frag in frag_done]
        return frag_done_l

class Report():
    """ produces some reports concerning the scanning of the poems """

    def test():
        print("in method test from class Report")

    @staticmethod
    def get_scans_frag(frag_id, user_id):
        qwry = """
select count(*), syllable_id, syllable from syllable left join annotation on syllable.id = annotation.syllable_id where annotation.fragment_done and syllable.frag_id = :frag_id and annotation.user_id = :user_id group by annotation.syllable_id;
"""
        res = db.session.execute(qwry, {'frag_id':frag_id, 'user_id' : user_id})
        scans = res.fetchall()
        #print("scans -> ", scans)
        syls = Report.get_syl_frag(frag_id)
        #we update the syls that are stressed with True and the count
        for scan in scans:
            syls[scan['syllable_id']]['cnt'] = scan[0]
            syls[scan['syllable_id']]['stress'] = True
        return syls

        
    @staticmethod
    def get_freq_stressed_frag(frag_id):
        qwry = """
select count(*), syllable_id, syllable from syllable left join annotation on syllable.id = annotation.syllable_id where annotation.fragment_done and syllable.frag_id = :frag_id group by annotation.syllable_id;
"""
        res = db.session.execute(qwry, {'frag_id':frag_id})
        scans = res.fetchall()
        #print("scans -> ", scans)
        syls = Report.get_syl_frag(frag_id)
        #we update the syls that are stressed with True and the count
        for scan in scans:
            syls[scan['syllable_id']]['cnt'] = scan[0]
            syls[scan['syllable_id']]['stress'] = True
        return syls
        
    @staticmethod
    def get_syl_frag(frag_id):
        """get all syllables of a fragment in the correct order """
        s = "select id, syllable from syllable where frag_id = :id order by \
        line_nbr,word_nbr,syll_nbr"
        res = db.session.execute(s, {'id':frag_id})
        syls = {}
        #we set stress to False for each syl in a fragment
        for syl in res:
            syls[syl['id']] = {'syl': syl['syllable'], 'stress':False, 'cnt':0}
        return syls

    @staticmethod
    def get_syl_story(story_id):
        """ get all syllables of a story """
        s = "select story_id, fragment.id, title, frag_nbr from fragment join story on story.id = fragment.story_id where story.id = :id"
        res = db.session.execute(s, {'id' : story_id})
        frags = res.fetchall()
        syl_st = {}
        for frag in frags:
            print(frag['id'])
            syl_st[frag['title'] + '_' + str(frag['frag_nbr'])] = Report.get_freq_stressed_frag(frag['id'])
        return syl_st
    
    @staticmethod
    def get_syl_all():
        """ get all syllables of all stories """
        s = "select * from story"
        res = db.session.execute(s)
        stories = res.fetchall()
        a_syls = {}
        for story in stories:
            syls = Report.get_syl_story(story['id'])
            a_syls.update(syls)
        return a_syls

    @staticmethod
    def res_to_csv(fname, res):
        with open(fname, 'w', newline='') as csvfile:
            fieldnames = ['title', 'syl', 'cnt', 'stress']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for title,rows in res.items():
                writer.writerow({'title':title})
                for syl_id, row in rows.items():
                    writer.writerow(row)
    @staticmethod
    def get_scans_user(user_id):
        """get all scans of a specified user (id). It will be stored in a dictionary, with the title and fragment number combined as key"""
        s = "select user_id, frag_id from fragmentdone where user_id = :user_id"
        res = db.session.execute(s, {'user_id':user_id})
        scans = res.fetchall()
        scans_st = {}
        for scan in scans:
            #first get the story id and title
            s = "select story_id, fragment.id, title, frag_nbr from fragment join story on story.id = fragment.story_id where fragment.id = :id"
            res = db.session.execute(s, {'id' : scan['frag_id']})
            story = res.fetchone()
            user_scan = Report.get_scans_frag(scan['frag_id'], user_id)
            #print(user_scan)
            scans_st[story['title'] + '_' + str(story['frag_nbr'])] = user_scan
        return scans_st
            
    @staticmethod
    def user_scans_to_file(user_id, filename):
        with open(filename, 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            data = Report.get_scans_user(user_id)
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        print("user scans for id %s have been written to %s" % (user_id, filename))

    @staticmethod
    def file_scans_to_dict(filename):
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        return data
