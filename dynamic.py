import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

import math

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

import storage, render, config

import simplejson as json

class Index(webapp.RequestHandler):
    def get(self, page):
        page = int(page) if page else 0
        self.response.headers['Content-Type'] = "text/html"
        posts = storage.list(config.posts_per_page*page, config.posts_per_page)
        number_of_posts = storage.count()
        number_of_pages = int(math.ceil(float(number_of_posts)/config.posts_per_page))
        metadata = {
                'page': page,
                'posts': number_of_posts, 
                'pages': number_of_pages
                }
        self.response.out.write(render.html_render(posts, metadata))
        
class Post(webapp.RequestHandler):
    def get(self, key):
        try:
            post = storage.get(key)
        except storage.DBException:
            self.error(404)
            return
        if post:
            self.response.headers['Content-Type'] = "text/html"
            self.response.out.write(render.html_render([post]))
        else:
            self.error(404)
      
class API(webapp.RequestHandler):
    def get(self, action):
        if action == "put":
            self.p_put()
        elif action == "get":
            self.p_get()
        elif action == "pop":
            self.p_pop()
    def post(self, action):
        self.get(action)
    def p_pop(self):
        self.response.headers["Content-Type"] = "application/json"
        if users.is_current_user_admin():
            storage.delete(self.request.get('key'))
            self.response.out.write(json.dumps({'status':'done'}))
        else:
            self.response.out.write(json.dumps({'status':'forbidden'}))
    def p_put(self):
        self.response.headers["Content-Type"] = "text/plain"
        user = users.get_current_user()
        if user:
            if users.is_current_user_admin():
                storage.put(self.request.get('title'),
                           self.request.get('content'),
                           self.request.get('format'),
                           self.request.get('key'))
                self.redirect("/")
            else:
                self.error(403)
        else:
            self.response.headers["Content-Type"] = "text/plain"
            self.response.out.write("You don't have permission to post here")
    def p_get(self):
        self.response.headers['Content-Type'] = "text/json"
        pp = storage.get(self.request.get('key'))
        p = {"title":pp.title, "content":pp.content,"key":str(pp.key()),"format":pp.format}
        self.response.out.write(json.dumps(p))
        
class Atom(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "application/atom+xml"
        posts = storage.list(0, config.posts_per_feed)
        self.response.out.write(render.atom_render(posts))      
            
                
      
application = webapp.WSGIApplication([(r'/([0-9])*', Index),
                                      (r'/post/(.*)', Post),
                                      (r'/api/(.*)', API),
                                      (r'/atom', Atom)])

if __name__ == "__main__":
    run_wsgi_app(application)
