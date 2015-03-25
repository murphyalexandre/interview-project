from datetime import datetime

from app import db


class Post(db.Model):
    __table_name__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    message = db.Column(db.String(120))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.String(255))

    # We use joined here since we assume there won't be that many comments
    # In case we need optimization, we could use dynamic.
    # https://pythonhosted.org/Flask-SQLAlchemy/models.html#one-to-many-relationships
    comments = db.relationship(
        'Comment', backref='post', lazy='joined')

    def __repr__(self):
        return '<Post {}>'.format(self.title)


class Comment(db.Model):
    __table_name__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(255))
    message = db.Column(db.String(120))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return '<Comment {}>'.format(self.author)
