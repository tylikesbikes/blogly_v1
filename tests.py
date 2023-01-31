from unittest import TestCase
from app import app
from models import db, connect_db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['FOLLOW_REDIRECTS'] = True

connect_db(app)

db.drop_all()

db.create_all()



class BloglyTestCase(TestCase):
    """Tests model for Blogly User"""
    def setUp(self):
        User.query.delete()
        app.config['TESTING'] = True
        self.client = app.test_client()

    def tearDown(self):

        db.session.rollback()

    def test_user_create(self):
        usr = User(first_name='tyler',last_name='dewitt',image_url='https://media.tenor.com/Yq9yVxw0CrkAAAAC/ski-skiing.gif')
        db.session.add(usr)
        db.session.commit()

        usr_from_db = User.query.all()
        self.assertEqual(usr_from_db[0].first_name, 'tyler')

    def test_base_route(self):
        usr1 = User(first_name='tyler',last_name='dewitt',image_url='some_url')
        usr2 = User(first_name='katie',last_name='dewitt',image_url='some_other_url')
        db.session.add(usr1)
        db.session.add(usr2)
        db.session.commit()

        with self.client as client:
            html_base = self.client.get('/',follow_redirects=True)
            html_redir = self.client.get('/users')

            self.assertIn(b'tyler',html_base.data)

            self.assertIn(b'<h1>Users</h1>',html_redir.data)
            self.assertIn(b'katie',html_redir.data)

    def test_add_user(self):
        with self.client as client:
            new_usr_data = {'first_name':'new', 'last_name':'user','image_url':'pic_url'}
            res = self.client.post('/users/new',follow_redirects=True, data=new_usr_data)

            self.assertIn(b'<h1>Users</h1>',res.data)
            self.assertIn(b'new user</a>',res.data)



    def test_add_user(self):
        with self.client as client:
            new_usr_data = {'first_name':'new', 'last_name':'user','image_url':'pic_url'}
            res = self.client.post('/users/new',follow_redirects=True, data=new_usr_data)

            self.assertIn(b'<h1>Users</h1>',res.data)
            self.assertIn(b'new user</a>',res.data)
        
    def test_delete_user(self):
        with self.client as client:
            usr1 = User(first_name='asdf',last_name='fdsatest',image_url='some_url')
            usr2 = User(first_name='katie',last_name='dewitt',image_url='some_other_url')
            db.session.add(usr1)
            db.session.add(usr2)
            db.session.commit()

            before_delete = self.client.get('/users')
            self.assertIn(b'katie',before_delete.data)

            after_delete = self.client.post(f'/users/{usr2.id}/delete',follow_redirects=True)
            self.assertNotIn(b'katie',after_delete.data)