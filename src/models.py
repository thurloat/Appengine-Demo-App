from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.api import mail

class Message(db.Model):
    """
        Data Model
    """
    body = db.TextProperty()
    date = db.DateTimeProperty(auto_now = True, auto_now_add = True)

    @classmethod
    def save_a_message(cls, body):
        """
            Saving a message!
        """
        message = Message()
        message.body = body
        message.save()
        memcache.delete("all_messages")

        mail.send_mail(sender = "adam@sheepdoginc.ca",
                       to = "adam@sheepdoginc.ca",
                       subject = "Long Messages Submitted",
                       body = """
Hi Adam! This is just a notification to let you know that a massive message was submitted to the MeetingApp. I had to defer it.
                       """)
