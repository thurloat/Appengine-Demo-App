"""
    High Performance Application with App Engine
    
    uses memcache, deferred commands
"""

from google.appengine.api import memcache
from google.appengine.ext import deferred, webapp, db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from models import Message
import logging
import os


class MainPage(webapp.RequestHandler):

    def get(self):
        """
            Fetch All Messages using memcache
        """

        messages = memcache.get("all_messages")

        if not messages:
            messages = Message.all().order("-date").fetch(20)
            memcache.add("all_messages", messages, 30)
            cache_hit = False
        else:
            cache_hit = True

        """
            Make Messages available to the template
        """
        context = {
            'messages': messages,
            'cache_hit': cache_hit
        }

        """
            Render Template
        """
        path = os.path.join(os.path.dirname(__file__), 'base.html')
        self.response.out.write(template.render(path, context))

class MessageHandler(webapp.RequestHandler):
    def post(self):
        """
            Handle the form post at /message
        """

        body = self.request.get('body')

        if len(body) > 10:
            """
                Huge body text, let's defer this command.
            """
            deferred.defer(Message.save_a_message, body, _countdown = 10)
        else:
            """
                Small enough, lets just save and return
            """
            Message.save_a_message(body)

        self.redirect("/")


"""
    Register the urls for the application
"""
application = webapp.WSGIApplication([('/', MainPage),
                                      ('/message', MessageHandler)], debug = True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
