from api_imports import *

import os
import uuid
import cloudstorage as gcs

from google.appengine.api import taskqueue

@endpoints.api(name='bills',
                version='v1',
                allowed_client_ids=[WEB_CLIENT_ID, API_EXPLORER_CLIENT_ID],
                scopes=[EMAIL_SCOPE])
class BillsApi(remote.Service):
    @endpoints.method(BillMessage, BillMessage,
            path='createBill',
            http_method='POST', name='createBill')
    def createBill(self,request):
        user = endpoints.get_current_user()
        raise_unless_user(user)

        accountId = request.accountId
        checkAccountAccess(user, accountId, settings.EDITOR_SCOPE)

        billId = str(uuid.uuid4())

        bill = Bill(
                id=billId,
                accountId=accountId,
                title=request.title,
                currency_code=request.currency_code,
                amount=float(request.amount),
                date=parser.parse(request.date),
                notes=request.notes,
                tagsHashString=arrayToHashString(extractArrayFromStringMessageArray(request.tags))
                )

        billFiles = self._buildBillFiles(request, billId)
        bill = Bill.createWithFiles(bill, billFiles)
        return buildBillMessage(bill)

    def _buildBillFiles(self,request, billId):
        accountId = request.accountId
        billFiles = []
        for staging_filepath in request.staging_filepaths:
            billFileId=str(uuid.uuid4())
            filepath = copyStagingFilepathToGcs(staging_filepath, accountId, billId, billFileId)
            billFiles.append(self._buildBillFile(
                id=billFileId,
                billId = billId,
                name = os.path.basename(filepath),
                path=filepath
                ))
        return billFiles

    def _buildBillFile(self,id,billId,name,path):
        billFile = BillFile(
                id=id,
                billId=billId,
                name=name,
                path=path
        )
        filestat = gcs.stat('/' + settings.FILE_BUCKET + path)
        billFile.file_type = filestat.content_type
        return billFile



    @endpoints.method(BillMessage, BillMessage,
            path='updateBill',
            http_method='POST', name='updateBill')
    def updateBill(self,request):
        user = endpoints.get_current_user()
        raise_unless_user(user)

        accountId = request.accountId
        checkAccountAccess(user, accountId, settings.EDITOR_SCOPE)

        bill = Bill.get(accountId, request.billId)
        bill.currency_code = request.currency_code
        bill.amount = float(request.amount)
        bill.title = request.title
        bill.date = parser.parse(request.date)
        bill.tagsHashString = arrayToHashString(extractArrayFromStringMessageArray(request.tags))

        bill = Bill.create(bill)

        return buildBillMessage(bill)

    @endpoints.method(BillMessage, BillMessage,
            path='deleteBill',
            http_method='POST', name='deleteBill')
    def deleteBill(self,request):
        user = endpoints.get_current_user()
        raise_unless_user(user)

        accountId = request.accountId
        checkAccountAccess(user, accountId, settings.EDITOR_SCOPE)

        bill = Bill.get(accountId, request.billId)
        bill = bill.delete()

        return buildBillMessage(bill)

    @endpoints.method(BillMessage, BillMessage,
            path='addFileToBill',
            http_method='POST', name='addFileToBill')
    def addFileToBill(self,request):
        user = endpoints.get_current_user()
        raise_unless_user(user)

        accountId = request.accountId
        checkAccountAccess(user, accountId, settings.EDITOR_SCOPE)

        billId = request.billId
        bill = Bill.get(accountId, billId)
        if bill:
            billFiles = self._buildBillFiles(request,billId)
            bill.addFiles(billFiles)
            bill = Bill.get(accountId, billId)
            return buildBillMessage(bill)


    @endpoints.method(BillMessage, BillMessage,
            path='removeFileFromBill',
            http_method='POST', name='removeFileFromBill')
    def removeFileFromBill(self,request):
        user = endpoints.get_current_user()
        raise_unless_user(user)

        accountId = request.accountId
        checkAccountAccess(user, accountId, settings.EDITOR_SCOPE)

        billId = request.billId
        bill = Bill.get(accountId, billId)

        if bill:
            bill.removeFile(request.billfileToDeleteId)
            bill = Bill.get(accountId, billId)
            return buildBillMessage(bill)


    @endpoints.method(BillMessage, BillMessage,
            path='getBill',
            http_method='POST', name='getBill')
    def getBill(self,request):
        user = endpoints.get_current_user()
        raise_unless_user(user)

        accountId = request.accountId
        checkAccountAccess(user, accountId, settings.EDITOR_SCOPE)
        bill = Bill.get(accountId, request.billId)

        return buildBillMessage(bill)


# Not really being used. Not sure how to post to an endpoint directly using a task queue.
    @endpoints.method(BillMessage, StringMessage,
            path='detectBillFileType',
            http_method='POST', name='detectBillFileType')
    def detectBillFileType(self,request):
        accountId = int(request.accountId)
        accountKey = Key(Account, accountId)
        billId = request.billId
        billKey = Key(Bill, billId, parent=accountKey)

        billfileId = request.billfileToDetect
        billFile = Key(BillFile, billfileId, parent=billKey).get()

        # Build file path
        filepath = getFilepath(str(accountId), billId, billfileId, billFile.name)
        filestat = gcs.stat('/' + settings.FILE_BUCKET + filepath)

        billFile.file_type = filestat.content_type
        billFile.put()

        return StringMessage(data = 'Detected:' + billFile.file_type)
