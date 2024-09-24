from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, func
import secrets

# CREATE DATABASE BASE CLASS
class Base(DeclarativeBase):
    pass

# Create the extension for SQLAlchemy
db = SQLAlchemy(model_class=Base)

# Define the User model
class User(db.Model):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    polls: Mapped[list['Poll']] = relationship('Poll', backref='creator', lazy='select')

    def __repr__(self):
        return f'<User {self.username}>'

# Define the Poll model
class Poll(db.Model):
    __tablename__ = 'poll'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question: Mapped[str] = mapped_column(String(255), nullable=False)
    options: Mapped[list['Option']] = relationship('Option', backref='poll', lazy='select')
    unique_id: Mapped[str] = mapped_column(String(16), unique=True, nullable=False, default=lambda: secrets.token_urlsafe(8))
    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Poll question={self.question}, unique_id={self.unique_id}>'

# Define the Option model
class Option(db.Model):
    __tablename__ = 'option'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(100), nullable=False)
    poll_id: Mapped[int] = mapped_column(Integer, ForeignKey('poll.id'), nullable=False)
    votes: Mapped[list['Vote']] = relationship('Vote', backref='option', lazy='select')
    
    @property
    def vote_count(self):
        # Efficient querying to get the count of votes
        return db.session.query(func.count(Vote.id)).filter_by(option_id=self.id).scalar()

# Define the Vote model
class Vote(db.Model):
    __tablename__ = 'vote'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    option_id: Mapped[int] = mapped_column(Integer, ForeignKey('option.id'), nullable=False)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)
   