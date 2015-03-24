from datetime import datetime

from app import db


class Post(db.Model):
    __table_name__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    message = db.Column(db.String(120))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.String(255))

    def __repr__(self):
        return '<Post {}>'.format(self.title)
