from protorpc import messages

class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    data = messages.StringField(1, required=True)

class ProfileMessage(messages.Message):
    userId = messages.StringField(1)
    nickname = messages.StringField(2)

class FileMessage(messages.Message):
    filename = messages.StringField(1)
    signed_url = messages.StringField(2)
    billfileId = messages.StringField(3)
    file_type = messages.StringField(4)
    thumbnail = messages.StringField(10)

class BillMessage(messages.Message):
    accountId = messages.StringField(1)

    billId = messages.StringField(2)
    title = messages.StringField(3)
    currency_code = messages.StringField(4)
    amount = messages.FloatField(5)
    date = messages.StringField(6)
    notes = messages.StringField(7)
    tags = messages.MessageField(StringMessage,8,repeated=True)

    day = messages.IntegerField(9)
    month = messages.IntegerField(10)
    year = messages.IntegerField(11)
    staging_filepaths = messages.MessageField(StringMessage,12,repeated=True)
    filepaths = messages.MessageField(StringMessage,13,repeated=True)
    files = messages.MessageField(FileMessage,14,repeated=True)
    deleted = messages.BooleanField(15)

    billfileToDeleteId = messages.StringField(50)
    billfileToDetect = messages.StringField(60)
    dateHuman = messages.StringField(70)

class AccountMessage(messages.Message):
    accountId = messages.StringField(1)
    name = messages.StringField(2)
    tagstr = messages.StringField(3)
    default_currency_code = messages.StringField(4)
    tags = messages.MessageField(StringMessage,5, repeated=True)
    editors = messages.MessageField(StringMessage,6, repeated=True)
    bills = messages.MessageField(BillMessage,7, repeated=True)

    # Non model attributes
    editorToAdd = messages.StringField(50)
    editorToRemove = messages.StringField(60)

    status_msg = messages.StringField(100)

class AccountListMessage(messages.Message):
    owner_accounts = messages.MessageField(AccountMessage,1,repeated=True)
    editor_accounts = messages.MessageField(AccountMessage,2,repeated=True)

class DayActivityMessage(messages.Message):
    date = messages.StringField(1)
    num_bills = messages.IntegerField(2)

class AccountActivityMessage(messages.Message):
    accountId = messages.StringField(1)
    name = messages.StringField(2)
    activity = messages.MessageField(DayActivityMessage,3,repeated=True)

class AccountsActivityMessage(messages.Message):
    data = messages.MessageField(AccountActivityMessage,1,repeated=True)

class SearchBillsRequest(messages.Message):
    accountId = messages.StringField(1)
    tags = messages.MessageField(StringMessage,2, repeated=True)
    start_date = messages.StringField(3)
    end_date = messages.StringField(4)
    query = messages.StringField(5)

class SearchBillsResponse(messages.Message):
    request = messages.MessageField(SearchBillsRequest,1)

    num_results = messages.IntegerField(2)
    results = messages.MessageField(BillMessage,3, repeated=True)

class UseInvitationMessage(messages.Message):
    invitationId = messages.StringField(1)

class StatusMessage(messages.Message):
    status = messages.StringField(1)
    message = messages.StringField(2)

