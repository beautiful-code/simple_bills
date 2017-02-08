# Ref: https://mail.python.org/pipermail/python-list/2012-January/618880.html
from api_imports import *

@endpoints.api(name='accounts',
                version='v1',
                allowed_client_ids=[WEB_CLIENT_ID, API_EXPLORER_CLIENT_ID],
                scopes=[EMAIL_SCOPE])
class AccountsApi(remote.Service):
    @endpoints.method(message_types.VoidMessage, AccountListMessage,
            path='listAccounts',
            http_method='POST', name='listAccounts')
    def listAccounts(self, request):
        user=endpoints.get_current_user()
        raise_unless_user(user)

        profile = userProfile(user)

        def _copyAccountMessage(account):
            am = AccountMessage()
            am.accountId = account.id
            am.name = account.name

            am.check_initialized()
            return am

        alm = AccountListMessage()
        for account in profile.Accounts:
            alm.owner_accounts.append(_copyAccountMessage(account))

        for account in profile.roleAccounts:
            alm.editor_accounts.append(_copyAccountMessage(account))

        alm.check_initialized()
        return alm

    @endpoints.method(AccountMessage, AccountMessage,
            path='createAccount',
            http_method='POST', name='createAccount')
    def createAccount(self,request):
        user=endpoints.get_current_user()
        raise_unless_user(user)

        profile = userProfile(user)

        account = Account(
                id = str(uuid.uuid4()),
                profileId = profile.id,
                name = request.name,
                tagstr = request.tagstr,
                defaultCurrencyCode = request.default_currency_code,
                )
        account = Account.create(account)

        return self._buildAccountMessage(account)


    @endpoints.method(AccountMessage, AccountMessage,
            path='updateAccount',
            http_method='POST', name='updateAccount')
    def updateAccount(self,request):
        user=endpoints.get_current_user()
        raise_unless_user(user)

        accountId = request.accountId
        checkAccountAccess(user, accountId, settings.FULL_SCOPE)

        account = Account.get(accountId)
        account.tagstr = request.tagstr
        account.name = request.name
        account.default_currency_code = request.default_currency_code
        account = Account.create(account)

        return self._buildAccountMessage(account)

    @endpoints.method(AccountMessage, AccountMessage,
            path='addEditor',
            http_method='POST', name='addEditor')
    def addEditor(self,request):
        user=endpoints.get_current_user()
        raise_unless_user(user)
        profile = userProfile(user)

        accountId = request.accountId
        checkAccountAccess(user, accountId, settings.FULL_SCOPE)
        account = Account.get(accountId)

        editor = request.editorToAdd
        editorProfile = Profile.get(editor)
        status_msg = None
        if not editorProfile:
            account.sendInvitation(profile.email,editor)
            status_msg = "Invitation sent to {}.".format(editor)
        else:
            account.addEditor(editorProfile)
            status_msg = "Account shared with {}.".format(editor)

        return self._buildAccountMessage(account, status_msg=status_msg)

    @endpoints.method(AccountMessage, AccountMessage,
            path='removeEditor',
            http_method='POST', name='removeEditor')
    def removeEditor(self,request):
        user=endpoints.get_current_user()
        raise_unless_user(user)

        accountId = request.accountId
        checkAccountAccess(user, accountId, settings.FULL_SCOPE)

        editor = request.editorToRemove
        account = Account.get(accountId)
        account.removeEditor(editor)

        return self._buildAccountMessage(account, status_msg = "Access removed for {}.".format(editor))


    @endpoints.method(AccountMessage, AccountMessage,
            path='getAccount',
            http_method='POST', name='getAccount')
    def getAccount(self,request):
        user=endpoints.get_current_user()
        raise_unless_user(user)

        accountId = request.accountId
        checkAccountAccess(user, accountId)
        account = Account.get(accountId)

        return self._buildAccountMessage(account)

    def _buildAccountMessage(self,account,status_msg = None):
        am = AccountMessage()
        am.accountId = account.id
        am.name = account.name
        am.tagstr = account.tagstr
        am.default_currency_code = account.defaultCurrencyCode
        am.editors = buildStringMessagesFromArray(account.editors())
        am.tags = buildStringMessagesFromArray(account.tags())
        if status_msg:
            am.status_msg = status_msg

        am.check_initialized()

        return am

    @endpoints.method(message_types.VoidMessage, AccountsActivityMessage,
            path='getAccountsActivity',
            http_method='POST', name='getAccountsActivity')
    def getAccountsActivity(self,request):
        user=endpoints.get_current_user()
        raise_unless_user(user)

        profile = userProfile(user)

        asam = AccountsActivityMessage()
        for account in profile.Accounts:

            aam = AccountActivityMessage()
            aam.accountId = account.id
            aam.name = account.name

            bills = account.lastNDayBills(30)

            # Build a hash of date and count
            activity = {}
            for bill in bills:
                bill_date = str(bill.date)
                day_activity = activity.get(bill_date, {'num_bills': 0})
                day_activity['num_bills'] +=1
                activity[bill_date] = day_activity

            for bill_date, value in activity.iteritems():
                # Build DayActivityMessages
                dam = DayActivityMessage()
                dam.date = bill_date
                dam.num_bills = value['num_bills']
                aam.activity.append(dam)

            aam.check_initialized()
            asam.data.append(aam)
        return asam
