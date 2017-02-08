import httplib2
import apiclient
import oauth2client
import os
import settings
import pprint
from google.appengine.api import urlfetch

from base import BaseHandler

CLIENT_ID = settings.WEB_CLIENT_ID
CLIENT_SECRET = settings.WEB_CLIENT_SECRET
SCOPE = 'https://www.googleapis.com/auth/userinfo.email'

class OAuth2CallbackPage(BaseHandler):
    def get(self):
        flow = oauth2client.client.OAuth2WebServerFlow(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            scope=SCOPE,
            # http://stackoverflow.com/questions/21097008/the-app-keeps-asking-for-permission-to-have-offline-access-why
            approval_prompt='auto',
            redirect_uri= '%s://%s%s' % (self.request.environ['wsgi.url_scheme'], self.request.environ['HTTP_HOST'], os.environ['OAUTH_REDIRECT_PATH'])
            )
        code = self.request.get('code')

        if not code:
            auth_uri = flow.step1_get_authorize_url()
            return self.redirect(auth_uri)
        else:
            credentials = flow.step2_exchange(self.request.get('code'))
            self.session['credentials'] = credentials.to_json()
            redirect_url = '/'
            if self.session.get('return_url'):
                redirect_url = str(self.session.get('return_url'))
                self.session['redirect_url'] = '/'

            return self.redirect(redirect_url)

def get_service(session, api_name, use_auth=True):

    # Build the service object
    api_root = '%s%s' % (os.environ['CRUDAPI_SERVER'], os.environ['API_ROOT_PATH'])
    api = api_name
    version = 'v1'
    discovery_url = '%s/discovery/v1/apis/%s/%s/rest' % (api_root, api, version)
    if use_auth:
        credentials = oauth2client.client.OAuth2Credentials.from_json(session.get('credentials'))
        http_auth = credentials.authorize(httplib2.Http(timeout=10))

        return apiclient.discovery.build(api_name, 'v1', discoveryServiceUrl=discovery_url, http=http_auth)
    else:
        return apiclient.discovery.build(api_name, 'v1', discoveryServiceUrl=discovery_url)


def check_credentials(func):
    """ Checks whether the session user has valid credentials """
    def wrapper(*args, **kwargs):
        page_handler = args[0]
        page_handler.session['return_url'] = page_handler.request.url

        session_credentials = get_session_credentials(page_handler)

        if not session_credentials:
            return page_handler.redirect('/oauth2callback')

        credentials = oauth2client.client.OAuth2Credentials.from_json(session_credentials)
        if credentials.access_token_expired:
            # TODO: Use the refresh token to fetch another access token.
            # http://stackoverflow.com/questions/27771324/google-api-getting-credentials-from-refresh-token-with-oauth2client-client
            return page_handler.redirect('/oauth2callback')

        return func(*args, **kwargs)
    return wrapper

def get_session_credentials(handler):
    return handler.session.get('credentials')

def is_user_logged_in(handler):
    session_credentials = get_session_credentials(handler)

    if session_credentials:
        credentials = oauth2client.client.OAuth2Credentials.from_json(session_credentials)
        if not credentials.access_token_expired:
            return True

    return False

# Revoke the Oauth token
# http://stackoverflow.com/questions/21405274/this-app-would-like-to-have-offline-access-when-access-type-online
def revoke_access_token(handler):
    session_credentials = get_session_credentials(handler)
    if session_credentials:
        credentials = oauth2client.client.OAuth2Credentials.from_json(session_credentials)
        urlfetch.fetch('%s?token=%s' % (credentials.revoke_uri, credentials.access_token))

    return True

