import logging
import endpoints
import cloudstorage as gcs

from google.appengine.api import images
from google.appengine.ext import blobstore

from google.appengine.api import users
from google.appengine.ext import ndb

from google.appengine.api import app_identity


import time
import urllib
from datetime import datetime, timedelta
import os
import base64
import uuid

GCS_ACCESS_ENDPOINT = 'https://storage.googleapis.com'


from models import *
from api_messages import *
import settings
from sql_models import *

def raise_unless_user(user):
    if not user:
        raise endpoints.UnauthorizedException('Authorization required')

def extractArrayFromStringMessageArray(list):
    result = []
    if list:
        for item in list:
            result.append(item.data)
    return result

def buildStringMessagesFromArray(array):
    result = []
    if array:
        for item in array:
            sm = StringMessage()
            sm.data = item
            result.append(sm)
    return result


def userProfile(user):
    if not user:
        raise users.UserNotFoundError("From userProfile(user)")
    user_email = user.email()

    session = Session()
    profile = session.query(Profile).filter(Profile.email == user_email).first()

    if not profile:
        profile = Profile(
            id = str(uuid.uuid4()),
            userId = user.user_id(),
            email = user_email,
            nickname = user.nickname()
        )
        session.add(profile)
        session.commit()
        logging.info('METRIC:USER_ADD - {}'.format(user_email))

    return profile

def checkAccountAccess(user, account_id, scope=settings.READ_SCOPE):
    profile = userProfile(user)
    account = Account.get(account_id)

    if profile.ownsAccount(account):
        return True

    if profile.editorOfAccount(account, scope):
        return True

    raise endpoints.InternalServerErrorException("{} tried to access account id {} with scope {}.".format(profile.email, account_id, scope))

def getFilepath(account_id, bill_id, bill_file_id, filename):
    return '/' + account_id + '/' + bill_id + '/' + bill_file_id + '/' + filename

def copyStagingFilepathsToGcs(request, account_id, bill_id, bill = None):
    filepaths = []
    for staging_filepath in request.staging_filepaths:
        filename = os.path.basename(staging_filepath.data)
        filepath = getFilepath(account_id, bill_id, filename)
        if bill and (filepath in bill.filepaths):
            raise endpoints.InternalServerErrorException("{} file already uploaded.".format(filename))
        filepaths.append(filepath)
        gcs.copy2(
                '/' + settings.STAGING_FILE_BUCKET + staging_filepath.data,
                '/' + settings.FILE_BUCKET + filepath)

    return filepaths

def copyStagingFilepathToGcs(staging_filepath, account_id, bill_id, bill_file_id):
    filename = os.path.basename(staging_filepath.data)
    filepath = getFilepath(account_id, bill_id, bill_file_id, filename)
    gcs.copy2(
            '/' + settings.STAGING_FILE_BUCKET + staging_filepath.data,
            '/' + settings.FILE_BUCKET + filepath)
    return filepath



def buildBillMessage(bill):
    bm = BillMessage()

    bm.billId = bill.id
    bm.title = bill.title
    bm.currency_code = bill.currency_code
    bm.amount = bill.amount
    bm.notes = bill.notes
    bm.date = str(bill.date)
    bm.dateHuman = bill.date.strftime("%b %d")
    bm.day = bill.day
    bm.month = bill.month
    bm.year = bill.year
    bm.deleted = bill.deleted

    for tag in hashStringToArray(bill.tagsHashString):
        sm = StringMessage()
        sm.data = tag
        bm.tags.append(sm)

    for billFile in bill.BillFiles:
        fm = FileMessage()
        fm.filename = billFile.name
        fm.signed_url= sign_url(billFile.path)
        fm.billfileId= billFile.id
        fm.file_type = billFile.file_type
        if fm.file_type in settings.SUPPORTED_IMAGE_FILE_TYPES:
            # Compute thumbnail
            blob_key = blobstore.create_gs_key('/gs/{}{}'.format(
                settings.FILE_BUCKET, billFile.path
                ))
            img_url = images.get_serving_url(blob_key=blob_key)
            fm.thumbnail = img_url + "=s128-c"

        bm.files.append(fm)

    return bm


# http://stackoverflow.com/questions/29847759/cloud-storage-and-secure-download-strategy-on-app-engine-gcs-acl-or-blobstore
# We dont have this working in development. Not really needed.
def sign_url(bucket_object, expires_after_seconds=300):
    method = 'GET'
    gcs_filename = urllib.quote('/%s%s' % (settings.FILE_BUCKET, bucket_object))
    content_md5, content_type = None, None

    expiration = datetime.datetime.utcnow() + timedelta(seconds=expires_after_seconds)
    expiration = int(time.mktime(expiration.timetuple()))

    # Generate the string to sign.
    signature_string = '\n'.join([
        method,
        content_md5 or '',
        content_type or '',
        str(expiration),
        gcs_filename])

    _, signature_bytes = app_identity.sign_blob(str(signature_string))
    signature = base64.b64encode(signature_bytes)

    # Set the right query parameters.
    query_params = {'GoogleAccessId': app_identity.get_service_account_name(),
                    'Expires': str(expiration),
                    'Signature': signature}

    # Return the download URL.
    return '{endpoint}{resource}?{querystring}'.format(endpoint=GCS_ACCESS_ENDPOINT,
                                                       resource=gcs_filename,
                                                       querystring=urllib.urlencode(query_params))


def hashStringToArray(hash_string):
    return [x for x in hash_string.split('##') if x]

def arrayToHashString(array):
    if not array:
        return ''
    return '##{}##'.format('##'.join(array))

