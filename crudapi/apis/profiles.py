from api_imports import *

@endpoints.api(name='profiles',
                version='v1',
                allowed_client_ids=[WEB_CLIENT_ID, API_EXPLORER_CLIENT_ID],
                scopes=[EMAIL_SCOPE])
class ProfilesApi(remote.Service):
    @endpoints.method(message_types.VoidMessage, ProfileMessage,
            path='getProfile',
            http_method='POST', name='getProfile')
    def getProfile(self, request):
        user = endpoints.get_current_user()
        raise_unless_user(user)
        profile = userProfile(user)

        pm = ProfileMessage()
        pm.userId = profile.userId
        pm.nickname = profile.nickname
        return pm


    @endpoints.method(UseInvitationMessage, StatusMessage,
            path='useInvitation',
            http_method='POST', name='useInvitation')
    def useInvitation(self, request):
        user = endpoints.get_current_user()
        raise_unless_user(user)
        profile = userProfile(user)

        invitation = Invitation.get(request.invitationId)

        sm = StatusMessage()
        if invitation.expired():
            sm.status = 'ERROR'
            sm.message = 'Your invitation is expired.'
        elif invitation.used():
            sm.status = 'ERROR'
            sm.message = 'The invitation code is already used.'
        else:
            account = Account.get(invitation.accountId)
            account.addEditor(profile)
            # TODO: Ideally the below command should in a transaction with the addEditor
            invitation.mark_used()

            sm.status = 'SUCCESS'
            sm.message = 'The account {} is now shared with you.'.format(account.name)
        return sm





