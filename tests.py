from unittest import TestCase

from app import app

from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()

db.create_all()

usr = User('tyler','dewitt','https://media.tenor.com/Yq9yVxw0CrkAAAAC/ski-skiing.gif')

class BloglyTestCase(TestCase):
    """Tests model for Blogly User"""
    def setUp(self):
        User.query.delete()

    def tearDown(self):

        db.session.rollback()

    def test_user_create(self):
        usr = User(first_name="Tyler", last_name="DeWitt", image_url="imgurl")
        self.assertEquals(usr.image_url, "imgurl")