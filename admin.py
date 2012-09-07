from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users


from os import path

import storage as storage
import logging


class Admin(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            if users.is_current_user_admin():
                self.response.headers['Content-Type'] = "text/html"
                self.response.out.write(open(path.join(path.dirname(__file__), "template", "admin.html")).read() %\
                                {'list':self.list(storage.list(0, 500)), 'nick': user.nickname(), 'mail': user.email()}) 
            else:
                self.redirect(users.create_login_url(self.request.uri))
        else:
            self.redirect(users.create_login_url(self.request.uri))
    def list(self, posts):
        htl = ""
        for post in posts:
            htl += "<li><a href='#%s' class='post' style='color: #87d5e9'>%s</a> (%s) <a href='#' style='color:red' class='delete'>[Delete post]</a></li>" % (str(post.key()), post.title, post.date)
        return htl

application = webapp.WSGIApplication([('/admin.*', Admin)])

if __name__ == "__main__":
    run_wsgi_app(application)
