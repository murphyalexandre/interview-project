import unittest

from app import app, db
from app.bulletin_board.models import Post


class IPTestCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.create_all()

    def test_index(self):
        rv = self.app.get('bulletin-board/', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Add a new post', rv.data)

    def test_add(self):
        rv = self.app.get('bulletin-board/add', follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'Title', rv.data)
        self.assertIn(b'Message', rv.data)

    def test_add_post(self):
        rv = self.app.post('bulletin-board/add', data=dict(
            title='A test title',
            message='A test message!'
        ), follow_redirects=True)
        self.assertIn(b'A test title', rv.data)
        self.assertIn(b'A test message!', rv.data)

    def test_post_model_date_created(self):
        post = Post(
            title='A test post',
            message='This is the message in my test post.',
        )
        db.session.add(post)
        db.session.commit()
        self.assertTrue(post.date_created)

    def tearDown(self):
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
