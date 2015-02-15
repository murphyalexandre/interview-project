from flask import Blueprint, render_template, abort, request, redirect
from jinja2 import TemplateNotFound

from app import db

from .models import Post

bulletin_board = Blueprint(
    'bulletin_board',
    __name__,
    template_folder='templates',
    url_prefix='/bulletin-board'
)


@bulletin_board.route('/', defaults={'page': 'index'}, methods=['GET'])
@bulletin_board.route('/<string:page>',  methods=['GET'])
def simple_page(page):
    try:
        data = {}
        if page == 'index':
            data['posts'] = Post.query.all()
        return render_template('{}.html'.format(page), **data)
    except TemplateNotFound:
        abort(404)


@bulletin_board.route('/add', methods=['POST'])
def add():
    post = Post(
        title=request.form['title'],
        message=request.form['message'],
    )
    db.session.add(post)
    db.session.commit()
    return redirect('/bulletin-board')

