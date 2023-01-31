from app import app

from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'

db = SQLAlchemy()

def connect_db(app):

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User info table"""

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key = True,
                   auto_increment = True)
    first_name = db.Column(db.String(20),
                           nullable = False)
    last_name = db.Column(db.String(35),
                          nullable = False)
    image_url = db.Column(db.String(500),
                          default='https://freeiconshop.com/wp-content/uploads/edd/gif-outline.png')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


db.app = app
db.init_app(app)
# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
katie = User(first_name='Katie', last_name='DeWitt',image_url='https://media.tenor.com/g6wy5gpkeFgAAAAC/brain.gif')
tyler = User(first_name='Tyler', last_name='Durden',image_url='https://media.tenor.com/ARyF_gaBqrYAAAAC/virus-soap.gif')
test_db_user = User(first_name='test', last_name='dbuser',image_url='https://media.tenor.com/g6wy5gpkeFgAAAAC/brain.gif')


# Add new objects to session, so they'll persist
db.session.add(katie)
db.session.add(tyler)
db.session.add(test_db_user)

# Commit--otherwise, this never gets saved!
db.session.commit()