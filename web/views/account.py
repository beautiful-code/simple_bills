from view_imports import *
import json

class CreateAccount(BaseHandler):
    @check_credentials
    def post(self):
        accounts_service = get_service(self.session, 'accounts')
        body = {
                'name': self.request.get('account_name'),
                'default_currency_code': self.request.get('account_default_currency_code'),
                'tagstr': self.request.get('account_tagstr')
                }
        response = accounts_service.createAccount(body=body).execute()

        self.redirect('/account/'+response['accountId'])

class AccountDetail(BaseHandler):
    @check_credentials
    def get(self, account_id):
        profiles_service = get_service(self.session, 'profiles')
        profile = profiles_service.getProfile().execute()

        account_service = get_service(self.session,'accounts')
        response = account_service.getAccount(body={'accountId':account_id}).execute()

        response_accounts = account_service.listAccounts().execute()
        account_tags = stringMessagesToList(response['tags'])
        account_tags_json = json.dumps(account_tags)

        stats_service = get_service(self.session, 'stats')
        stats_response = stats_service.accountStatsOnDemand(body={'accountId':account_id}).execute()

        has_bills = True if int(stats_response['bill_count']) > 0 else False

        template_values = {
            'profile' : profile,
            'account_id': response['accountId'],
            'account_name': response['name'],
            'account_tags': account_tags,
            'account_tags_json': account_tags_json,
            'has_bills': has_bills,
            'default_currency_code': response.get('default_currency_code') or '',
            'supported_currencies': settings.SUPPORTED_CURRENCIES,
            'account_default_currency_code': response.get('default_currency_code'),
            'owner_accounts': response_accounts.get('owner_accounts') or [],
            'editor_accounts': response_accounts.get('editor_accounts') or [],
            'stats': stats_response,
            'stats_json': json.dumps(stats_response),
            'flash_msg': self.session.get_flashes()
        }
        template = JINJA_ENVIRONMENT.get_template('account_detail.html')
        self.response.out.write(template.render(template_values))

class AccountSettings(BaseHandler):
    @check_credentials
    def get(self, account_id):
        profiles_service = get_service(self.session, 'profiles')
        profile = profiles_service.getProfile().execute()

        account_service = get_service(self.session,'accounts')
        response = account_service.getAccount(body={'accountId':account_id}).execute()

        response_accounts = account_service.listAccounts().execute()
        template_values = {
                'account': response,
                'account_id': account_id,
                'name': response.get('name'),
                'tagstr': response.get('tagstr') or '',
                'supported_currencies': settings.SUPPORTED_CURRENCIES,
                'default_currency_code': response.get('default_currency_code') or '',
                'flash_msg': self.session.get_flashes(),
        }

        template = JINJA_ENVIRONMENT.get_template('account_settings.html')
        self.response.out.write(template.render(template_values))

    @check_credentials
    def post(self, account_id):
        account_service = get_service(self.session,'accounts')
        response = account_service.updateAccount(
                body={
                    'accountId': account_id,
                    'name': self.request.get('account_name'),
                    'tagstr': self.request.get('account_tagstr'),
                    'default_currency_code': self.request.get('account_default_currency_code')
                    }
                ).execute()

        self.redirect(self.request.path)

class AddEditor(BaseHandler):
    @check_credentials
    def post(self, account_id):
        account_service = get_service(self.session,'accounts')
        response = account_service.addEditor(
                body={
                    'accountId': account_id,
                    'editorToAdd': self.request.get('account_editor_to_add')
                    }
                ).execute()
        self.session.add_flash(response['status_msg'])

        self.redirect(self.request.referer)


class RemoveEditor(BaseHandler):
    @check_credentials
    def post(self, account_id):
        account_service = get_service(self.session,'accounts')
        response = account_service.removeEditor(
                body={
                    'accountId': account_id,
                    'editorToRemove': self.request.get('account_editor_to_remove')
                    }
                ).execute()
        self.session.add_flash(response['status_msg'])

        self.redirect(self.request.referer)
