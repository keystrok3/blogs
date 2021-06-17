
""" All The routes used for the api are here """

from flask import request, jsonify, make_response
from . import api
import jwt
import datetime

from .. import create_app

from flask_httpauth import HTTPBasicAuth

app = create_app('default')     # application instance for use in taking configuration values
auth = HTTPBasicAuth()


from app.models import User, Post
from app import db
from functools import wraps


''' Decorator To View Functions of Protected Routes '''
def token_required(f): 
    @wraps(f)
    def decorated_fxn(*args, **kwargs):
        token = None
        
        # generate token for logged in users
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({"message": "token missing"}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(username=data['username']).first()
        except:
            return jsonify({'message': 'token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated_fxn

# Register new user
@api.route('/register', methods=['POST', 'GET'])
def register():
    data = request.get_json()
    
    user = User(username=data['username'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'new user added'})

# User Login
@api.route('/login', methods=['POST', 'GET'])
def login():
    auth = request.authorization
    
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate', 'Basic realm="login required"'})
    
    user = User.query.filter_by(username=auth.username).first()
    
    if user and user.verify_password(auth.password) :
        token = jwt.encode({'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    else:
        return make_response('Could not verify', 401, {'WWW-Authenticate', 'Basic realm="login required"'})
    
    

# get all posts
@api.route('/allposts', methods=['GET'])
def allposts():
    posts = Post.query.all()
    
    allposts = dict()
    for post in posts:
        author = User.query.filter_by(id=post.author_id).first()
        title = post.title,
        body = post.body
        
        allposts[post.id] = {
            'author': author.username,
            'title': title,
            'body': body,
        }
        
    return jsonify(allposts)

# create new post
@api.route('/newpost', methods=['POST', 'GET'])
@token_required
def newpost(current_user):    
    post = Post()
    post.author_id = current_user.id
    post.title = request.form['title']
    post.body = request.form['body']
    
    db.session.add(post)
    db.session.commit()
    
    return jsonify({"message": "Successful"}), 200

# delete post
@api.route('/deletepost/<int:id>', methods=['POST'])
@token_required
def deletepost(current_user, id):
    del_post = Post.query.filter_by(author_id=current_user.id).first()
    if not del_post: 
        return jsonify({"message": "No Such Post"})
    
    try:
        db.session.delete(del_post)
        db.session.commit()
    except:
        return jsonify({"message": "Error"})
    
    return jsonify({"message": "Successfully Removed"})



# Edit post
@api.route('/editpost/<int:id>', methods=['PUT'])
@token_required
def editpost(current_user, id):
    ed_post = Post.query.filter_by(author_id=current_user.id).first()
    
    if not ed_post:
        return jsonify({"message": "No such post"})
    
    ed_post.title = request.form['title']
    ed_post.body = request.form['body']
    
    db.session.add(ed_post)
    db.session.commit()
    
    return jsonify({"message": "Post updated"})