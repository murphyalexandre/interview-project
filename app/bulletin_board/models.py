from datetime import datetime

from app import db


class Post(db.Model):
    __table_name__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    message = db.Column(db.String(120))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', foreign_keys=user_id)

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
    message = db.Column(db.String(120))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', foreign_keys=user_id)

    def __repr__(self):
        return '<Comment {}>'.format(self.author)


class User(db.Model):
    __table_name__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def get_id(self):
        return self.email

    def is_active(self):
        return True

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False
