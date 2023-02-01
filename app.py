from flask import Flask, render_template, redirect, request
# from flask_debugtoolbar import DebugToolbarExtension
from models import User, Post, db, connect_db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'keeta'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)

connect_db(app)

app.app_context().push()


@app.route('/')
def redirect_to_users():
    """Redirect to users list """

    return redirect('/users')

@app.route('/users')
def show_users():
    """Show list of users"""
    users = User.query.order_by(User.last_name).order_by(User.first_name).all()

    return render_template('users_homepage.html', users = users)

@app.route('/users/new',methods=['GET'])
def add_user_form():
    """Show a form to add a new user"""
    return render_template('add_user.html')

@app.route('/users/new', methods=['POST'])
def create_new_user():
    """Add a new user from the add user form"""
    fname = request.form['first_name']
    lname = request.form['last_name']
    imgurl = request.form['image_url'] if request.form['image_url'] != '' else None

    new_user = User(first_name=fname, last_name=lname, image_url=imgurl)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:usrid>')
def view_user(usrid):
    """Show a specific user page"""

    user_info = User.query.get(usrid)
    user_posts = Post.query.filter_by(user_id_fk=usrid)

    return render_template('user_info.html',user = user_info, user_id = usrid, posts = user_posts)

@app.route('/users/<int:user_id>/edit',methods=['GET'])
def edit_user_info(user_id):
    """Show a page to edit user info"""

    user = User.query.get(user_id)

    return render_template('edit_user.html',user = user, user_id = user_id)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user_info(user_id):
    """Get form data from edit user page and update db"""
    fname = request.form['first_name']
    lname = request.form['last_name']
    imgurl = request.form['image_url'] if request.form['image_url'] != '' else 'https://freeiconshop.com/wp-content/uploads/edd/gif-outline.png'
    
    db.session.rollback()

    user = User.query.get(user_id)

    user.first_name = fname
    user.last_name = lname
    user.image_url = imgurl

    db.session.add(user)
    db.session.commit()

    return redirect('/')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete user from db"""
    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return redirect('/')

@app.route('/users/<int:user_id>/posts/new', methods=['GET'])
def new_post_form(user_id):
    """Show the form to add a new post"""
    user = User.query.get(user_id)
    return render_template('create_post.html', user = user)
    

@app.route('/users/<int:usrid>/posts/new', methods=['POST'])
def create_new_post(usrid):
    """Create a new blog post from the form at create_post.html"""

    post_title = request.form['post_title']
    post_content = request.form['post_content']

    new_post = Post(title=post_title, content = post_content, user_id_fk = usrid)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{usrid}')
    
@app.route('/posts/<int:postid>', methods=['GET'])
def show_post(postid):
    """Show Post"""

    this_post = Post.query.get(postid)
    post_author = User.query.get(this_post.user_id_fk)
    

    return render_template('show_post.html',post = this_post, author=post_author)

@app.route('/posts/<int:postid>/delete',methods=['POST'])
def delete_post(postid):
    """Delete Post and return to original author's page"""

    #get user id from original post
    this_post = Post.query.get(postid)
    post_author = User.query.get(this_post.user.id).id

    post_to_delete = Post.query.filter(Post.id == postid).delete()
    db.session.commit()

    return redirect(f'/users/{post_author}')
    
@app.route('/posts/<int:postid>/edit',methods=['GET'])
def edit_post_form(postid):
    """Show form to edit a post"""

    post = Post.query.get(postid)
    author = User.query.get(post.user.id)

    return render_template('edit_post.html',post=post, author=author)

@app.route('/posts/<int:postid>/edit',methods=['POST'])
def update_post(postid):    
    """Commit post changes to db"""
    post_title = request.form['post_title']
    post_content = request.form['post_content']

    this_post = Post.query.get(postid)
    this_post.title = post_title
    this_post.content = post_content

    db.session.add(this_post)
    db.session.commit()

    return redirect(f'/posts/{postid}')