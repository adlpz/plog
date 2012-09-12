from google.appengine.ext import db
from google.appengine.api import users
from datetime import datetime


class DBException(Exception):
    pass

class Post(db.Model):
    title = db.StringProperty()
    author = db.UserProperty()
    content = db.TextProperty()
    format = db.StringProperty()
    date = db.DateTimeProperty()
    
def put(title, content, format, key=None, author=users.get_current_user(), date=datetime.now()):
    if key:
        p = Post.get(key)
        if not p:
            p = Post()
    else:
        p = Post()
    p.title = title
    p.author = author
    p.content = content
    p.format = format
    p.date = date
    p.put()

def get(key):
    try:
        return Post.get(key)
    except db.BadKeyError:
        raise DBException
        
def delete(key):
    e = get(key)
    if e:
        e.delete()
def list(offset, count):
    q = Post.all()
    q.order("-date")
    return q.fetch(count, offset)

def count():
    return Post.all().count()
