from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    entries = db.relationship('Entry', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Comment {}>'.format(self.id)


tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey(
                    'tag.id'), primary_key=True),
                db.Column('entry_id', db.Integer, db.ForeignKey(
                    'entry.id'), primary_key=True)
                )


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    content = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tag', secondary=tags, backref="entries")
    comments = db.relationship('Comment', backref='entry', lazy=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Entry {}>'.format(self.title)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Tag {}>'.format(self.description)
