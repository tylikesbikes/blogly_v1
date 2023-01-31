from flask_sqlalchemy import SQLAlchemy

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