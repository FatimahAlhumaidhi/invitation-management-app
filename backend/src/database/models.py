import os
from sqlalchemy import Column, String, Integer, Boolean, create_engine
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    '''
      setup_db(app)
          binds a flask application and a SQLAlchemy service
    '''
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    '''
      db_drop_and_create_all()
          drops the database tables and starts fresh
          can be used to initialize a clean database
    '''
    db.drop_all()
    db.create_all()
    # add one demo row which is helping in POSTMAN test



class Invitation(db.Model):
    '''
      Invitation
      Represents a wedding invitation.

          id (primary key): Unique identifier for the invitation.
          name: Name of the invited guest.
          email: Email address of the invited guest.
          plus_one: Boolean indicating whether the guest is allowed to bring a plus one.
    '''
    __tablename__ = 'invitations'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False)
    text = Column(String(500), nullable=False)
    rsvps = db.relationship('RSVP', backref='invitation', lazy=True)

    def __init__(self, name, email, text=False):
        self.name = name
        self.email = email
        self.text = text

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }


class RSVP(db.Model):
    '''
      RSVP
      Represents an RSVP response to a wedding invitation.
        
        id (primary key): Unique identifier for the RSVP.
        invitation_id: Foreign key referencing the Invitation model.
        response: String representing the guest's response to the invitation (e.g. "Attending", "Not Attending", "Undecided").
        guest_name: Name of the guest who is responding to the invitation.
        guest_email: Email address of the guest who is responding to the invitation.
    ''' 
    __tablename__ = 'rsvps'

    id = Column(Integer, primary_key=True)
    jwt_sub = Column(Integer, nullable=False)
    response = Column(String(120), nullable=False)
    guest_name = Column(String(120), nullable=False)
    guest_email = Column(String(120), unique=True, nullable=False)
    invitation_id = Column(Integer, db.ForeignKey('invitations.id'), nullable=False)

    def __init__(self, invitation_id, response, guest_name, guest_email, jwt_sub):
        self.invitation_id = invitation_id
        self.response = response
        self.guest_name = guest_name
        self.guest_email = guest_email
        self.jwt_sub = jwt_sub

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'jwt_sub': self.jwt_sub,
            'invitation_id': self.invitation_id,
            'response': self.response,
            'guest_name': self.guest_name if self.guest_name else None,
            'guest_email': self.guest_email if self.guest_email else None
        }
