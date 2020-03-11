from dataclasses import dataclass
from datetime import datetime
from referencecreator import db, login_manager  # Why does it not find these?
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@dataclass
class User(db.Model, UserMixin):
    # id: int
    # username: str

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    project = db.relationship('Project', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# association_table = Table('ProjectToReference', Base.metadata, Column('project_id', Integer,
# ForeignKey('project.id')), Column('reference_id', Integer, ForeignKey('reference.id')))


@dataclass  # using dataclass you don't need to have the serialize function
class Project(db.Model):
    # but you need to identify the types of the fields
    # id: int
    # title: str
    # date_created: datetime
    # user: User

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship(User)
    # reference = relationship("Reference", secondary=association_table)

    def __repr__(self):
        return f"Project ('{self.title}' created on '{self.date_created}')"

    # but with the serialize() allows you to get information from relationships
    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'user': self.user_id,
            'username': self.user.username
        }


@dataclass
class Reference(db.Model):
    """id: int
    title: str
    author: str
    publish_date: datetime
    subtitle: str
    journal_title: str
    volume: int
    number: int
    page_start: int
    page_end: int
    doi: str
    isbn: str
    chapter: str
    editor: str
    publish_place: str
    publisher: str
    url: str
    organisation: str"""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    publish_date = db.Column(db.DateTime)
    subtitle = db.Column(db.String(200))
    author = db.Column(db.String(200))
    journal_title = db.Column(db.String())
    volume = db.Column(db.Integer)
    number = db.Column(db.Integer)
    pages = db.Column(db.String(10))
    doi = db.Column(db.String(50))
    isbn = db.Column(db.String(100))
    chapter = db.Column(db.String(100))
    editor = db.Column(db.String(150))
    publish_place = db.Column(db.String(100))
    publisher = db.Column(db.String(150))
    url = db.Column(db.String(300))
    organisation = db.Column(db.String(100))


@dataclass
class ProjectToReference(db.Model):
    # id: int
    # user: User
    # project = Project

    id = db.Column(db.Integer, primary_key=True)
    retrieve_date = db.Column(db.DateTime, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
    project = relationship(Project)
    reference_id = db.Column(db.Integer, db.ForeignKey('reference.id'), primary_key=True)
    reference = relationship(Reference)


@dataclass
class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_expired = db.Column(db.DateTime, nullable=False)
    token = db.Column(db.String(60), nullable=False, index=True)  # index helps searching
