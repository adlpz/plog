#plog


#What?

Plog is a super-lightweight dynamic blog engine but still with a decent enough administration interface. 
So no editing plain text files through SSH, no. It's designed to be a drop-in solution for having a free little
blog running on Google's budget under the free tier of App Engine, and autoescalate if you become a rockstar, I
suppose.

So it's built around Google App Engine's Datastore, but should be easy to port to other storage models and DBs. The framework
is the integrated Webapp, but there's a stand-alone version [here](http://webapp-improved.appspot.com/), so it
should be trivial to run anywhere else.

**Features**

* Easy configuration through one file. No database set up (yay Datastore!)
* **Markdown syntax**
* Atom feed
* **Code syntax highlightling** (http://code.google.com/p/google-code-prettify/)
* Kick-ass JS admin interface
* **Easy customization through a single [Mustache](http://mustache.github.com/) template**
* Google-provided account management and security, so I don't have to write safe code.

**Drawbacks**

* No comment feature. Just use twitter for feedback!
* Needs a Google Account for authentication.

**Dependencies**

* [Pystache](https://github.com/defunkt/pystache), a python implementation of the Mustache templating system.
* [simplejson](https://github.com/simplejson/simplejson), a streamlined JSON library for Python.
* [rfc3339](https://bitbucket.org/henry/rfc3339/src), for Atom-compatible datetime format. **Included with Plog**.

You can install this dependencies in your system or just drop the packages in the **lib/** directory.

#Story?

I've been using custom made blog engines for ages, just because I was there when the most commonly used 
(*cough cough Wordpress*) were being hacked like it was christmas. Also because I'm usually bored.

This is just the packaging of what I've been using over http://prealfa.com/blog. I might improve it somehow
so it can be useful for people else than me.

#Usage?

Drop in a App Engine instance. Edit config.py to your liking. Go to http://your\_blog/admin. Write things. Make it pretty
editing the css if you feel like.

#Screenshots


## Default theme
![Default theme](http://i.imgur.com/8NsjW.png)

## Admin interface
![Admin interface](http://i.imgur.com/9gvIo.png)
