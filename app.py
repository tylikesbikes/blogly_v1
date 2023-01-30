from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import User, db, connect_db, get_user_by_id

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'keeta'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

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

@app.route('/users/<int:user_id>')
def view_user(user_id):
    """Show a specific user page"""

    user = User.query.get(user_id)

    return render_template('user_info.html',user = user, user_id = user_id)

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