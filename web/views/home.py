from view_imports import *
import json
import urllib2

class MainPage(BaseHandler):
    def get(self):
        home = '/me'

        if is_user_logged_in(self):
            self.redirect(home)
        else:
            template_values = {
                'login_url': home
            }

            template = JINJA_ENVIRONMENT.get_template('main.html')
            self.response.out.write(template.render(template_values))

class HomePage(BaseHandler):
    @check_credentials
    def get(self):
        profiles_service = get_service(self.session, 'profiles')
        profile = profiles_service.getProfile().execute()

        accounts_service = get_service(self.session, 'accounts')
        response = accounts_service.listAccounts().execute()

        #accounts_activity = accounts_service.getAccountsActivity().execute()

        template_values = {
            'profile': profile,
            'owner_accounts': response.get('owner_accounts') or [],
            'editor_accounts': response.get('editor_accounts') or [],
            'supported_currencies': settings.SUPPORTED_CURRENCIES,
            #'accounts_activity': accounts_activity,
            #'accounts_activity_json': json.dumps(accounts_activity),
            'flash_msg': self.session.get_flashes()
        }

        template = JINJA_ENVIRONMENT.get_template('home.html')
        self.response.out.write(template.render(template_values))

class LogoutPage(BaseHandler):
    def get(self):
        if is_user_logged_in(self):
            #revoke_access_token(self)
            self.session['credentials'] = None

        self.redirect('/')

class FeedbackPage(BaseHandler):
    @check_credentials
    def post(self):
        profiles_service = get_service(self.session, 'profiles')
        profile = profiles_service.getProfile().execute()

        data = {
            'note': self.request.get('feedback_desc'),
            'user': profile['nickname']
        }

        req = urllib2.Request('https://feedback-dash.herokuapp.com/feedbacks')
        req.add_header('Content-Type', 'application/json')

        response = urllib2.urlopen(req, json.dumps(data))

        self.session.add_flash('Your feedback is received. Thank you.')
        self.redirect(self.request.referer)

class UseInvitation(BaseHandler):
    @check_credentials
    def get(self,invitation_id):
        profiles_service = get_service(self.session, 'profiles')
        profile = profiles_service.getProfile().execute()

        response = profiles_service.useInvitation(
                body = {
                    'invitationId': invitation_id
                    }
                ).execute()


        self.session.add_flash(response['message'])
        self.redirect('/me')
