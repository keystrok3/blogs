
""" 
    Database Models.
    The Models are SQLAlchemy representations of the sqlite database in the system.
    
"""

from app import create_app, db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author')
    

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    ''' turns every string that comes into the password field into a hashed string '''
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    ''' verifies that the string entered into the password filed matches the relevant hash '''
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(64))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    


app = create_app('default')
app.app_context().push()
db.create_all()
    
    