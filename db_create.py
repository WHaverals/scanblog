from app import db
from app.models import User
import os.path
db.create_all()

#create allready a username for wouter, who will manage all the other users
user = User(username="wouter", email="wouter.haverals@uantwerpen.be")
user.set_password('Mavahmine')
db.session.add(user)
db.session.commit()
