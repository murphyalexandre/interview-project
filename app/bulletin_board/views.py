from flask import abort, Blueprint, flash, g, render_template, request, \
    redirect
from jinja2 import TemplateNotFound
from flask.ext.login import current_user, login_required, login_user, \
    logout_user

from app import bcrypt, db, login_manager

from .models import Comment, Post, User
from .forms import AddPostForm, LoginForm, RegistrationForm

bulletin_board = Blueprint(
    'bulletin_board',
    __name__,
    template_folder='templates',
    url_prefix='/bulletin-board'
)


# Needed by flask_login to reload user from session
@login_manager.user_loader
def load_user(user_email):
    return User.query.filter_by(email=user_email).first()


@bulletin_board.before_request
def before_request():
    g.user = current_user


@bulletin_board.route('/', methods=['GET'])
def simple_page():
    try:
        # Limiting to 5 recent posts
        data = {
            'posts': Post.query.order_by(Post.date_created.desc()).limit(5),
        }

        data['user'] = g.user if g.user is not None and \
            g.user.is_authenticated() else None

        return render_template('index.html', **data)
    except TemplateNotFound:
        abort(404)


@bulletin_board.route('/view/<int:post_id>',  methods=['GET'])
def view(post_id):
    data = {
        'post': Post.query.get_or_404(post_id)
    }
    return render_template('view.html', **data)


@bulletin_board.route('/edit/<int:post_id>',  methods=['GET', 'POST'])
@login_required
def edit(post_id):
    if g.user is None or not g.user.is_authenticated():
        flash('You need to be logged in to do this.')
        return redirect('/bulletin-board')

    post = Post.query.get_or_404(post_id)

    form = AddPostForm(obj=post)
    if form.validate_on_submit():
        post_id = request.form['id']
        post = Post.query.get_or_404(post_id)
        post.title = request.form['title']
        post.message = request.form['message']
        db.session.commit()
        return redirect('/bulletin-board')

    return render_template('edit.html', form=form, post=post)


@bulletin_board.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if g.user is None or not g.user.is_authenticated():
        flash('You need to be logged in to do this.')
        return redirect('/bulletin-board')

    form = AddPostForm()
    if form.validate_on_submit():
        post = Post(
            title=request.form['title'],
            message=request.form['message'],
            user=g.user
        )
        db.session.add(post)
        db.session.commit()
        return redirect('/bulletin-board')

    return render_template('add.html', form=form)


@bulletin_board.route('/comment', methods=['POST'])
@login_required
def comment():
    if request.method == 'POST':
        post_id = int(request.form['id'])
        post = Post.query.get_or_404(post_id)

        comment = Comment(
            message=request.form['message'],
            user=g.user
        )

        post.comments.append(comment)

        db.session.add(comment)
        db.session.commit()

        return redirect('/bulletin-board/view/{}'.format(post_id))


@bulletin_board.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_exists = User.query.filter_by(email=form.email.data).first()
        if user_exists is None:
            user = User(
                email=form.email.data,
                username=form.username.data,
                password=bcrypt.generate_password_hash(form.password.data)
            )

            db.session.add(user)
            db.session.commit()

            flash('Thank you for registering. You can now login.')

            return redirect('/bulletin-board/login')
        else:
            flash('User with that email already exists.')

            return redirect('/bulletin-board/register')

    return render_template("register.html", form=form)


@bulletin_board.route("/login", methods=["GET", "POST"])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect('/bulletin-board')

    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True

                db.session.add(user)
                db.session.commit()

                login_user(user, remember=True)

                return redirect('/bulletin-board')
            else:
                flash('Incorrect email / password combination')
        else:
            flash('User not found')

    return render_template("login.html", form=form)


@bulletin_board.route("/logout")
@login_required
def logout():
    logout_user()

    return redirect('/bulletin-board')
