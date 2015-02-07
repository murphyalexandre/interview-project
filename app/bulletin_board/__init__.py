from flask import Blueprint, render_template, abort, request, redirect, url_for
from jinja2 import TemplateNotFound

bulletin_board = Blueprint(
    'bulletin_board',
    __name__,
    template_folder='templates',
    url_prefix='/bulletin-board'
)

posts = [
    {'name': 'Post A', 'content': 'First post!'},
    {'name': 'Post B', 'content': 'lalalala'},
]

@bulletin_board.route('/', defaults={'page': 'index'}, methods=['GET'])
@bulletin_board.route('/<string:page>',  methods=['GET'])
def simple_page(page):
    try:
        data = {}
        if page == 'index':
            data['posts'] = posts
        return render_template('{}.html'.format(page), **data)
    except TemplateNotFound:
        abort(404)


@bulletin_board.route('/add', methods=['POST'])
def add():
    global posts
    new_post = {
        'name': request.form['name'],
        'content': request.form['content'],
    }
    posts.append(new_post)
    return redirect('/bulletin-board')
