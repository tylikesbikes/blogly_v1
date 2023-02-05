from flask import Flask, render_template, redirect, request
# from flask_debugtoolbar import DebugToolbarExtension
from models import User, Post, db, connect_db, dt, Post, Tag, PostTag
from other_functions import show_friendly_date

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'keeta'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)

connect_db(app)

app.app_context().push()


####  GETLIST testing
# @app.route('/tttesting', methods=['GET','POST'])
# def tttest():
#     if request.method=='GET':
#         return render_template('tttestlist.html')
#     elif request.method=='POST':
#         checkboxes = []
#         for s in request.form.getlist('cb'):
#             checkboxes.append(s)

#     return checkboxes




####

@app.route('/')
def redirect_to_users():
    """Show top 5 posts and a link to users page """

    recent_5_posts = Post.query.order_by(Post.created_at.desc()).limit(5)
    
    return render_template('home.html',posts = recent_5_posts, friendly_date = show_friendly_date)

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
    # user_posts = Post.query.filter_by(user_id_fk=usrid)
    user_posts = user_info.posts

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
    tags = Tag.query.all()

    return render_template('create_post.html', user = user, tags = tags)
    

@app.route('/users/<int:usrid>/posts/new', methods=['POST'])
def create_new_post(usrid):
    """Create a new blog post from the form at create_post.html"""

    post_title = request.form['post_title']
    post_content = request.form['post_content']

    dates = dt.now()
    print(dates)

    new_post = Post(title=post_title, content = post_content, user_id_fk = usrid, created_at = dt.now())

    db.session.add(new_post)
    db.session.commit()

    existing_tag_ids = db.session.query(Tag.id).all()
    post_tags = []

    for tag in existing_tag_ids:
        if request.form.get(str(tag[0])):
            post_tags.append(tag[0])

    for tag in post_tags:
        t = PostTag(post_id = new_post.id, tag_id = tag)
        db.session.add(t)
        db.session.commit()

    return redirect(f'/users/{usrid}')
    
@app.route('/posts/<int:postid>', methods=['GET'])
def show_post(postid):
    """Show Post"""

    this_post = Post.query.get(postid)
    post_author = User.query.get(this_post.user_id_fk)
    friendly_date = this_post.created_at
    friendly_date = show_friendly_date(friendly_date)

    tags = this_post.tags
    if len(tags) == 0:
        tags = None
    

    return render_template('show_post.html',post = this_post, author=post_author, friendly_date = friendly_date, tags = tags)

@app.route('/posts/<int:postid>/delete',methods=['POST'])
def delete_post(postid):
    """Delete Post and return to original author's page"""

    #get user id from original post
    this_post = Post.query.get(postid)
    post_author = User.query.get(this_post.user.id).id

    posttags = PostTag.query.filter_by(post_id = this_post.id).delete()

    post_to_delete = Post.query.filter(Post.id == postid).delete()
    db.session.commit()

    return redirect(f'/users/{post_author}')
    
@app.route('/posts/<int:postid>/edit',methods=['GET'])
def edit_post_form(postid):
    """Show form to edit a post"""

    post = Post.query.get(postid)
    author = User.query.get(post.user.id)
    applied_tags = Post.query.get(postid).tags
    all_tags = Tag.query.all()



    return render_template('edit_post.html',post=post, author=author, applied_tags= applied_tags, all_tags = all_tags)

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

    existing_tag_ids = db.session.query(Tag.id).all()
    post_tags = []

    PostTag.query.filter_by(post_id = postid).delete()
    db.session.commit()

    for tag in existing_tag_ids:
        if request.form.get(str(tag[0])):
            post_tags.append(tag[0])

    for tag in post_tags:
        t = PostTag(post_id = postid, tag_id = tag)
        db.session.add(t)
        db.session.commit()

    return redirect(f'/posts/{postid}')

@app.route('/tags',methods=['GET'])
def view_tags():
    """Show list of existing tags with links for more details about each"""

    tags = Tag.query.all()

    return render_template('view_tags.html', tags = tags)

@app.route('/tags/new', methods=['GET'])
def create_tag_form():
    """Show a form to create a new tag"""

    return render_template('new_tag.html')

@app.route('/tags/new', methods=['POST'])
def create_new_tag():
    """Create a new tag in the db"""

    tag_name = request.form['new_tag_name']

    new_tag = Tag(name=tag_name)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>', methods=['GET'])
def tag_detail(tag_id):
    """Show details for a tag along with an edit button"""
    tag = Tag.query.get(tag_id)

    posts_with_tag = tag.tagged_posts

    return render_template('tag_detail.html', tag = tag, posts = posts_with_tag)

@app.route('/tags/<int:tag_id>/edit', methods=['GET'])
def edit_tag_form(tag_id):
    """Show form to edit tag"""
    tag = Tag.query.get(tag_id)

    return render_template('edit_tag.html',tag = tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    tag = Tag.query.get(tag_id)

    tag.name = request.form['tag_name']

    db.session.add(tag)
    db.session.commit()
    return redirect(f'/tags/{tag_id}')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    
    Tag.query.filter(Tag.id == tag_id).delete()

    db.session.commit()

    return redirect('/tags')

@app.errorhandler(404)
def page_not_found(e):
    return "Custom 404:  The route you tried to access either doesn't exist or uses in invalid user id or post id", 404