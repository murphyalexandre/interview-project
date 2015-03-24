import unittest

from app import app, db
from app.bulletin_board.models import Post


class IPTestCase(unittest.TestCase):

    def add_post(self, title, message, author):
        post = Post(
            title=title,
            message=message,
            author=author
        )

        db.session.add(post)
        db.session.commit()

        return post

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.create_all()

        # Create at least one post
        self.add_post(
            title='Some Title', message='Some Message', author='Someone')

    def test_index(self):
        rv = self.app.get('bulletin-board/', follow_redirects=True)

        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Add a new post', rv.data)

        # We have at least our post
        self.assertIn(b'Some Title', rv.data)
        self.assertIn(b'Some Message', rv.data)
        self.assertIn(b'Someone', rv.data)

    def test_add(self):
        rv = self.app.get('bulletin-board/add', follow_redirects=True)

        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Title', rv.data)
        self.assertIn(b'Message', rv.data)
        self.assertIn(b'Author', rv.data)

    def test_add_post(self):
        rv = self.app.post('bulletin-board/add', data=dict(
            title='A test title',
            message='A test message!',
            author='A Person'
        ), follow_redirects=True)

        self.assertIn(b'A test title', rv.data)
        self.assertIn(b'A test message!', rv.data)
        self.assertIn(b'A Person', rv.data)

    def test_add_post_empty(self):
        rv = self.app.post(
            'bulletin-board/add', data=dict(), follow_redirects=True)

        self.assertEqual(rv.status_code, 400)

    def test_post_model_date_created(self):
        post = self.add_post(
            title='A test post',
            message='This is the message in my test post.',
            author='A Person')

        self.assertTrue(post.date_created)

    def test_edit_without_id(self):
        rv = self.app.get('bulletin-board/edit', follow_redirects=True)

        self.assertEqual(rv.status_code, 404)

    def test_edit(self):
        rv = self.app.get('bulletin-board/edit/1', follow_redirects=True)

        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Author', rv.data)
        self.assertIn(b'Title', rv.data)
        self.assertIn(b'Message', rv.data)
        self.assertIn(b'Someone', rv.data)
        self.assertIn(b'Some Title', rv.data)
        self.assertIn(b'Some Message', rv.data)

    def test_edit_post(self):
        rv = self.app.post('bulletin-board/edit/1', data=dict(
            id=1,
            title='A test title',
            message='A test message!',
            author='A Person'
        ), follow_redirects=True)

        self.assertIn(b'A test title', rv.data)
        self.assertIn(b'A test message!', rv.data)
        self.assertIn(b'A Person', rv.data)

    def test_edit_post_empty(self):
        rv = self.app.post(
            'bulletin-board/edit/1', data=dict(), follow_redirects=True)

        self.assertEqual(rv.status_code, 400)

    def tearDown(self):
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
