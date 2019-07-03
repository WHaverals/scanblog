from app import app, db
from app.models import User, Annotation, Story, Syllable, Fragment, Scanned, Report
import pprint

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Annotation=Annotation, Story=Story, Fragment=Fragment, Scanned=Scanned, Syllable=Syllable, Report=Report)
