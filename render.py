from os import path
from google.appengine.api import urlfetch
import urllib

import rfc3339
import pystache

import config 

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

def template_render(template, _posts):
    posts = [{
        'key'     : str(post.key()),
        'title'   : post.title.encode("utf-8"),
        'content' : Format.by_name(post.format)(post.content.encode("utf-8")),
        'date'    : post.date,
        'updated' : rfc3339.rfc3339(post.date),
        'url'     : path.join(config.base_url, 'posts',  str(post.key()))
        } for post in _posts]
    variables = {
            'blog_name'   : config.blog_name,
            'author'      : config.author,
            'email'       : config.email,
            'license'     : config.license,
            'plog_version': config.plog_version,
            'posts'       : posts,
            'updated'     : posts[0]['updated'] if len(posts) else 0
            }
    variables['title'] = posts[0]['title'] if len(posts) == 1 else ""
    return pystache.render(template, variables)

def html_render(posts):
    template = open(path.join(path.dirname(__file__), "template", "index.html")).read()
    return template_render(template, posts)

def atom_render(posts):
    template = open(path.join(path.dirname(__file__), "template", "atom.xml")).read()
    return template_render(template, posts)
