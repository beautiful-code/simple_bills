import webapp2
import os

from base import BaseHandler
from oauth import OAuth2CallbackPage
from views import *


config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': os.environ['WEB_SESSION_SECRET'],
}

app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/oauth2callback', OAuth2CallbackPage),
  ('/me', HomePage),
  ('/logout', LogoutPage),
  ('/feedback', FeedbackPage),
  ('/create_account', CreateAccount),
  ('/account/([^/]*)?', AccountDetail),
  ('/account/(.*)?/settings', AccountSettings),
  ('/account/(.*)?/add_editor', AddEditor),
  ('/account/(.*)?/remove_editor', RemoveEditor),
  ('/account/(.*)?/create_bill', CreateBill),
  ('/account/(.*)?/search_bills', SearchBill),
  ('/account/(.*)?/(.*)?/edit_bill', EditBill),
  ('/account/(.*)?/(.*)?/add_file', AddFileToBill),
  ('/account/(.*)?/(.*)?/delete', DeleteBill),
  ('/account/(.*)?/(.*)?/(.*)?/remove_file', RemoveFileFromBill),
  ('/account/(.*)?/(.*)?/(.*)?/detect_file_type', DetectBillFileType),
  ('/useinvitation/([^/]*)?', UseInvitation),
], debug=True, config=config)


def main():
  application.RUN()

if __name__ == '__main__':
  main()
