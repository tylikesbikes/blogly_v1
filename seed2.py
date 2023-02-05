from app import app

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime as dt

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
    
    posts = db.relationship('Post')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
class Post(db.Model):
    """Blog posts"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key = True,
                   auto_increment = True)
    title = db.Column(db.Text,
                      nullable = False)
    content = db.Column(db.Text,
                        nullable = False)
    created_at = db.Column(db.DateTime,
                           nullable = False)
    user_id_fk = db.Column(db.Integer,
                        db.ForeignKey('users.id'))
    
    user = db.relationship('User',backref='post')
    tags = db.relationship('Tag',
                            secondary='posttags',
                            backref='tagged_posts')
    

class Tag(db.Model):
    """Tags that can be added to posts"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key = True,
                   auto_increment = True)
    
    name = db.Column(db.Text,
                     unique = True)
    
    posts_with_tag = db.relationship('PostTag',backref='posts_by_tag')
    
    
class PostTag(db.Model):
    """List of posts w/tags associated with them"""

    __tablename__ = 'posttags'

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key = True,
                        )
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key = True)


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


# Add new user objects to session, so they'll persist
db.session.add(katie)
db.session.add(tyler)
db.session.add(test_db_user)

#Add posts
ty_post_1 = Post(title='First post', content='Hello world, first post!', created_at=dt.now(), user_id_fk=2)
db.session.add(ty_post_1)

#Add Tags
tag1 = Tag(name='Happy')
tag2 = Tag(name='Funny')
db.session.add(tag1)
db.session.add(tag2)

#PostTags
posttag1 = PostTag(post_id=1,tag_id=2)
db.session.add(posttag1)


# Commit--otherwise, this never gets saved!
db.session.commit()