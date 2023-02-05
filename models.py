from flask_sqlalchemy import SQLAlchemy
from other_functions import show_friendly_date
from datetime import datetime as dt

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
    
    posts = db.relationship('Post', backref='user', cascade='all, delete')

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
                        db.ForeignKey('users.id', ondelete='cascade'))
    
    # user = db.relationship('User',backref='post',cascade='all, delete-orphan')
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
    
    # post_tags = db.relationship('PostTag',backref='post_tags')                          # This will show a list of post/tag relationships in the PostTag table for a given tag
    # posts_by_tag = db.relationship('Post',                
    #                                  secondary = 'posttags', backref='posts_by_tag')    # This will show a list of posts that have this tag on them

    
    
class PostTag(db.Model):
    """List of posts w/tags associated with them"""

    __tablename__ = 'posttags'

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key = True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key = True)



#######ORIGINAL MODELS################
# class User(db.Model):
#     """User info table"""

#     __tablename__ = 'users'

#     id = db.Column(db.Integer,
#                    primary_key = True,
#                    auto_increment = True)
#     first_name = db.Column(db.String(20),
#                            nullable = False)
#     last_name = db.Column(db.String(35),
#                           nullable = False)
#     image_url = db.Column(db.String(500),
#                           default='https://freeiconshop.com/wp-content/uploads/edd/gif-outline.png')

#     @property
#     def full_name(self):
#         return f'{self.first_name} {self.last_name}'
    
# class Post(db.Model):
#     """Blog posts"""

#     __tablename__ = 'posts'

#     id = db.Column(db.Integer,
#                    primary_key = True,
#                    auto_increment = True)
#     title = db.Column(db.Text,
#                       nullable = False)
#     content = db.Column(db.Text,
#                         nullable = False)
#     created_at = db.Column(db.DateTime,
#                            nullable = False)
#     user_id_fk = db.Column(db.Integer,
#                         db.ForeignKey('users.id'))
#     user = db.relationship('User',backref='post')

#     tags = db.relationship('Tag',backref='posts')


# class Tag(db.Model):
#     """Tags that can be added to posts"""

#     __tablename__ = 'tags'

#     id = db.Column(db.Integer,
#                    primary_key = True,
#                    auto_increment = True)
    
#     name = db.Column(db.Text,
#                      unique = True)
    
#     posts = db.relationship('Post',backref='tags')
    
# class PostTag(db.Model):
#     """List of posts w/tags associated with them"""

#     __tablename__ = 'posttags'

#     post_id = db.Column(db.Integer,
#                         db.ForeignKey('posts.id'),
#                         primary_key = True,
#                         )
#     tag_id = db.Column(db.Integer,
#                        db.ForeignKey('tags.id'),
#                        primary_key = True)