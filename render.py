from os import path
from google.appengine.api import urlfetch
import urllib
from lib.rfc3339 import rfc3339
import config as config


class Format:
    @classmethod
    def by_name(self, name):
        try:
            m = getattr(self, name)
            return m if m else self.plain
        except AttributeError:
            return self.plain
    @classmethod
    def plain(self, content):
        return content
    @classmethod
    def markdown(self, content):
        """We rely on the Markdown service markdown-service.appspot.com"""
        return urlfetch.fetch("http://markdown-service.appspot.com/markdown",
                              payload=urllib.urlencode({"content":content}),
                              method=urlfetch.POST,
                              headers={'Content-Type': 'application/x-www-form-urlencoded'}).content

class Atom:
    def __init__(self):
        self.template = open(path.join(path.dirname(__file__), "template", "atom.xml")).read()
    def render(self, posts):
        entries = ""
        for post in posts:
            entry = "<entry><title>%(title)s</title>" + \
        "<link href=\"" + config.base_url + "/post/%(key)s\" />" + \
        "<id>" + config.base_url + "/post/%(key)s</id>" + \
        "<updated>%(updated)s</updated>" + \
        "<summary>%(content)s</summary></entry>"
            entries += entry % ({'title':post.title, 'updated': rfc3339(post.date),'key':str(post.key()), 'content':post.content[0:140 if 140 < len(post.content) else len(post.content)]})

        updated = rfc3339(posts[0].date) if len(posts) else 0;
        return self.template % {'base_url':config.base_url, 'blog_name': config.blog_name, 'author':config.author, 'email':config.email, 'updated':updated, 'entries':entries}
    
class HTML:
    def __init__(self):
        self.header_t = open(path.join(path.dirname(__file__), "template", "header.html")).read()
        self.post_t = open(path.join(path.dirname(__file__), "template", "post.html")).read() 
        self.footer_t = open(path.join(path.dirname(__file__), "template", "footer.html")).read() 
    def render(self, posts):
        html = self.header(posts[0].title if len(posts) == 1 else "")
        for post in posts:
            html += self.post(post)
        html += self.footer()
        return html
    def post(self, post):
        h = self.post_t % {'key': post.key(), 'title': post.title.encode("utf-8"),
                           'content':Format.by_name(post.format)(post.content.encode("utf-8")),
                           'date':post.date, 'base_url' : config.base_url}
        return h
    def header(self, title=""):
        return self.header_t % {'base_url': config.base_url, 'title': title, 'blog_name' : config.blog_name}
    def footer(self):
        return self.footer_t % {'blog_name': config.blog_name, 'email' : config.email, 'author': config.author, 'license': config.license_str}
