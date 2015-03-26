import unittest

from app import app, bcrypt, db
from app.bulletin_board.models import Post, Comment, User


class IPTestCase(unittest.TestCase):
    """
    Our test cases. This should probably be splitted in multiple files.
    """

    def add_post(self, title, message, user):
        post = Post(
            title=title,
            message=message,
            user=user
        )

        db.session.add(post)
        db.session.commit()

        return post

    def add_comment(self, message, user, post=None):
        comment = Comment(
            message=message,
            user=user
        )

        if post:
            post.comments.append(comment)

        db.session.add(comment)
        db.session.commit()

        return comment

    def add_user(self, username, email, password):
        user = User(
            email=email,
            username=username,
            password=bcrypt.generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        return user

    def login(self, email, password):
        return self.app.post('bulletin-board/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def fast_login(self):
        return self.login(
            email='some@email.com', password='asdfasdf')

    def logout(self):
        return self.app.get('bulletin-board/logout', follow_redirects=True)

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        db.create_all()

        # Create one user
        self.user = self.add_user(
            username='username',
            email='some@email.com',
            password='asdfasdf')

        # Create at least one post with a comment and one without
        post = self.add_post(
            title='Some Title', message='Some Message', user=self.user)
        self.add_comment(message='Some Comment', user=self.user, post=post)
        self.add_post(
            title='Title No Comments', message='No Comments', user=self.user)

    def tearDown(self):
        db.drop_all()

    # TESTS
    def test_index_limit(self):
        self.add_post(
            title='Title No Comments1',
            message='No Comments1', user=self.user)
        self.add_post(
            title='Title No Comments2',
            message='No Comments2', user=self.user)
        self.add_post(
            title='Title No Comments3',
            message='No Comments3', user=self.user)
        self.add_post(
            title='Title No Comments4',
            message='No Comments4', user=self.user)
        self.add_post(
            title='Title No Comments5',
            message='No Comments5', user=self.user)
        self.add_post(
            title='Title No Comments6',
            message='No Comments6', user=self.user)

        rv = self.app.get('bulletin-board/', follow_redirects=True)

        self.assertEqual(rv.status_code, 200)

        # We only have the latest 5 posts
        self.assertIn(b'username', rv.data)
        self.assertIn(b'Title No Comments6', rv.data)
        self.assertIn(b'No Comments6', rv.data)
        self.assertIn(b'Title No Comments5', rv.data)
        self.assertIn(b'No Comments5', rv.data)
        self.assertIn(b'Title No Comments4', rv.data)
        self.assertIn(b'No Comments4', rv.data)
        self.assertIn(b'Title No Comments3', rv.data)
        self.assertIn(b'No Comments3', rv.data)
        self.assertIn(b'Title No Comments2', rv.data)
        self.assertIn(b'No Comments2', rv.data)

    def test_index(self):
        rv = self.app.get('bulletin-board/', follow_redirects=True)

        self.assertEqual(rv.status_code, 200)

        # We have at least our post
        self.assertIn(b'Some Title', rv.data)
        self.assertIn(b'Some Message', rv.data)
        self.assertIn(b'username', rv.data)

    def test_add(self):
        rv = self.fast_login()
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Welcome, username!', rv.data)

        rv = self.app.get('bulletin-board/add', follow_redirects=True)

        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Title', rv.data)
        self.assertIn(b'Message', rv.data)

    def test_add_post(self):
        rv = self.fast_login()
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Welcome, username!', rv.data)

        rv = self.app.post('bulletin-board/add', data=dict(
            title='A test title',
            message='A test message!'
        ), follow_redirects=True)

        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'A test title', rv.data)
        self.assertIn(b'A test message!', rv.data)
        self.assertIn(b'username', rv.data)

    def test_add_post_empty(self):
        rv = self.fast_login()
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Welcome, username!', rv.data)

        rv = self.app.post(
            'bulletin-board/add', data=dict(), follow_redirects=True)

        self.assertEqual(rv.status_code, 400)

    def test_post_model_date_created(self):
        rv = self.fast_login()
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Welcome, username!', rv.data)

        post = self.add_post(
            title='A test post',
            message='This is the message in my test post.',
            user=self.user)

        self.assertTrue(post.date_created)

    def test_edit_without_id(self):
        rv = self.fast_login()
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Welcome, username!', rv.data)

        rv = self.app.get('bulletin-board/edit', follow_redirects=True)

        self.assertEqual(rv.status_code, 404)

    def test_edit(self):
        rv = self.fast_login()
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Welcome, username!', rv.data)

        rv = self.app.get('bulletin-board/edit/1', follow_redirects=True)

        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Title', rv.data)
        self.assertIn(b'Message', rv.data)
        self.assertIn(b'Some Title', rv.data)
        self.assertIn(b'Some Message', rv.data)

    def test_edit_post(self):
        rv = self.fast_login()
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Welcome, username!', rv.data)

        rv = self.app.post('bulletin-board/edit/1', data=dict(
            id=1,
            title='A test title',
            message='A test message!'
        ), follow_redirects=True)

        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'A test title', rv.data)
        self.assertIn(b'A test message!', rv.data)
        self.assertIn(b'username', rv.data)

    def test_edit_post_empty(self):
        rv = self.fast_login()
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Welcome, username!', rv.data)

        rv = self.app.post(
            'bulletin-board/edit/1', data=dict(), follow_redirects=True)

        self.assertEqual(rv.status_code, 400)

    def test_view_without_id(self):
        rv = self.fast_login()
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Welcome, username!', rv.data)

        rv = self.app.get('bulletin-board/view', follow_redirects=True)

        self.assertEqual(rv.status_code, 404)

    def test_view(self):
        rv = self.fast_login()
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Welcome, username!', rv.data)

        rv = self.app.get('bulletin-board/view/1', follow_redirects=True)

        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Some Title', rv.data)
        self.assertIn(b'Some Message', rv.data)
        self.assertIn(b'username', rv.data)
        self.assertIn(b'Comments', rv.data)
        self.assertIn(b'Some Comment', rv.data)
        self.assertIn(b'Enter a comment', rv.data)
        self.assertIn(b'username', rv.data)

    def test_view_no_comment(self):
        rv = self.fast_login()
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Welcome, username!', rv.data)

        rv = self.app.get('bulletin-board/view/2', follow_redirects=True)

        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Title No Comments', rv.data)
        self.assertIn(b'No Comments', rv.data)
        self.assertIn(b'Comments', rv.data)
        self.assertIn(b'Enter a comment', rv.data)
        self.assertIn(b'Be the first to comment on this post.', rv.data)

    def test_comment_empty(self):
        rv = self.fast_login()
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Welcome, username!', rv.data)

        rv = self.app.post(
            'bulletin-board/comment', data=dict(), follow_redirects=True)

        self.assertEqual(rv.status_code, 400)

    def test_comment(self):
        rv = self.fast_login()
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Welcome, username!', rv.data)

        rv = self.app.post('bulletin-board/comment', data=dict(
            id=1,
            message='Another Comment'
        ), follow_redirects=True)

        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Some Title', rv.data)
        self.assertIn(b'Some Message', rv.data)
        self.assertIn(b'username', rv.data)
        self.assertIn(b'Comments', rv.data)
        self.assertIn(b'username', rv.data)
        self.assertIn(b'Enter a comment', rv.data)
        self.assertIn(b'Some Comment', rv.data)
        self.assertIn(b'Another Comment', rv.data)

    def test_login(self):
        rv = self.app.get('bulletin-board/login', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

        self.assertIn(b'email', rv.data)
        self.assertIn(b'password', rv.data)

    def test_login_post(self):
        rv = self.fast_login()
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Welcome, username!', rv.data)

    def test_login_empty(self):
        rv = self.login(
            email='', password='')
        self.assertEqual(rv.status_code, 200)

        self.assertIn(b'email', rv.data)
        self.assertIn(b'password', rv.data)
        self.assertIn(b'This field is required', rv.data)

    def test_login_unknown(self):
        rv = self.login(
            email='asd@asd.com', password='asd')
        self.assertEqual(rv.status_code, 200)

        self.assertIn(b'email', rv.data)
        self.assertIn(b'password', rv.data)
        self.assertIn(b'User not found', rv.data)

    def test_login_wrong_pw(self):
        rv = self.login(
            email='some@email.com', password='asdaa')
        self.assertEqual(rv.status_code, 200)

        self.assertIn(b'email', rv.data)
        self.assertIn(b'password', rv.data)
        self.assertIn(b'Incorrect email / password combination', rv.data)

    def test_login_valid_email(self):
        rv = self.login(
            email='some', password='asdaa')
        self.assertEqual(rv.status_code, 200)

        self.assertIn(b'email', rv.data)
        self.assertIn(b'password', rv.data)
        self.assertIn(b'Invalid email address', rv.data)

    def test_login_valid_email2(self):
        rv = self.login(
            email='some@some', password='asdaa')
        self.assertEqual(rv.status_code, 200)

        self.assertIn(b'email', rv.data)
        self.assertIn(b'password', rv.data)
        self.assertIn(b'Invalid email address', rv.data)

    def test_logout(self):
        rv = self.fast_login()
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Welcome, username!', rv.data)

        rv = self.app.get('bulletin-board/logout', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

        self.assertNotIn(b'Welcome, username!', rv.data)

        # We have at least our post
        self.assertIn(b'Some Title', rv.data)
        self.assertIn(b'Some Message', rv.data)
        self.assertIn(b'username', rv.data)

    def test_logout_not_logged_in(self):
        rv = self.app.get('bulletin-board/logout', follow_redirects=True)
        self.assertEqual(rv.status_code, 401)

    def test_register(self):
        rv = self.app.get('bulletin-board/register', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

        self.assertNotIn(b'Welcome, username!', rv.data)

        # We have at least our post
        self.assertIn(b'Username', rv.data)
        self.assertIn(b'Email Address', rv.data)
        self.assertIn(b'New Password', rv.data)
        self.assertIn(b'Repeat Password', rv.data)
        self.assertIn(b'I accept the TOS', rv.data)
        self.assertIn(b'Register', rv.data)

    def test_register_empty(self):
        rv = self.app.post('bulletin-board/register', data=dict(
            username='',
            email='',
            password='',
            confirm='',
            accept_tos=False
        ), follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

        self.assertIn(
            b'Field must be between 4 and 25 characters long', rv.data)
        self.assertIn(b'Invalid email address', rv.data)
        self.assertIn(
            b'Field must be between 6 and 255 characters long', rv.data)
        self.assertIn(b'This field is required', rv.data)

    def test_register_post(self):
        return self.app.post('bulletin-board/register', data=dict(
            username='hello',
            email='hello@hello.com',
            password='asdfasdf',
            confirm='asdfasdf',
            accept_tos=True
        ), follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

        self.assertNotIn(b'Welcome, hello!', rv.data)


if __name__ == '__main__':
    unittest.main()
