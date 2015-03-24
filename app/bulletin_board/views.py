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


@bulletin_board.route('/', methods=['GET'])
def simple_page():
    try:
        data = {
            'posts': Post.query.all()
        }
        return render_template('index.html', **data)
    except TemplateNotFound:
        abort(404)


@bulletin_board.route('/edit/<int:post_id>',  methods=['GET', 'POST'])
def edit(post_id):
    if request.method == 'POST':
        post_id = request.form['id']
        post = Post.query.get_or_404(post_id)
        post.title = request.form['title']
        post.message = request.form['message']
        db.session.commit()
        return redirect('/bulletin-board')

    data = {
        'post': Post.query.get_or_404(post_id)
    }
    return render_template('edit.html', **data)


@bulletin_board.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        post = Post(
            title=request.form['title'],
            message=request.form['message'],
        )
        db.session.add(post)
        db.session.commit()
        return redirect('/bulletin-board')

    return render_template('add.html')
