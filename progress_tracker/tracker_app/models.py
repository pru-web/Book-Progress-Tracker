# CREATED TABLES FOR USERS, ADMIN, BOOKS,TRACKER USING SQLALCHEMY

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from .auth import hash_password

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    readlist = relationship('Tracker', back_populates='user',cascade='all, delete-orphan')
    # passwords are automatically hashed when creating or updating a users
    def set_password(self, password):
        self.password = hash_password(password)

class Admin(Base):
    __tablename__ = 'admin'
    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)

class Book(Base):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    authors = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=True)
    publish_year = Column(Integer, nullable=True)
    rating = Column(Float, nullable=True)
    pages = Column(Integer, nullable=True)

class Tracker(Base):
    __tablename__ = 'tracker'
    tracker_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    book_id = Column(Integer, ForeignKey('books.book_id'))
    status = Column(String)
    progress = Column(Integer)
    user = relationship('User', back_populates='readlist')
    book = relationship('Book')
    tracker_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    # This relationship is many-to-one, so no cascade settings
    user = relationship('User', back_populates='readlist', single_parent=True)

engine = create_engine('sqlite:///C:/progress_tracker_project/progress_tracker/progress_tracker/progress_tracker.db')
